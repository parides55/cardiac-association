import json
import logging

import cloudinary
import cloudinary.utils
from cloudinary import CloudinaryResource
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.views.decorators.http import require_POST

from .models import (
    People, Gallery, GalleryImage, GalleryVideo,
    image_url, video_poster_url,
)

logger = logging.getLogger(__name__)

ADMIN_THUMB = dict(width=120, height=90, crop="fill", gravity="auto",
                    quality="auto", fetch_format="auto")


def gallery_upload_folder(gallery_id):
    """Cloudinary folder that holds everything uploaded to one album."""
    return f"gallery/{gallery_id}"


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 0
    fields = ("preview", "image", "caption", "order")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        if not obj.pk or not obj.image:
            return ""
        return format_html(
            '<img src="{}" width="120" height="90" loading="lazy" alt=""><br>Photo #{}',
            image_url(obj.image, **ADMIN_THUMB), obj.pk,
        )


class GalleryVideoInline(admin.TabularInline):
    model = GalleryVideo
    extra = 0
    fields = ("preview", "video", "caption", "order")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        if not obj.pk or not obj.video:
            return ""
        return format_html(
            '<img src="{}" width="120" height="90" loading="lazy" alt=""><br>Video #{}',
            video_poster_url(obj.video, **ADMIN_THUMB), obj.pk,
        )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    change_form_template = "admin/about_us/gallery/change_form.html"
    inlines = [GalleryImageInline, GalleryVideoInline]
    list_display = ("title", "order", "photo_count", "video_count", "created_at")
    list_editable = ("order",)
    search_fields = ("title",)
    fields = ("title", "description", "cover_image", "order")

    @admin.display(description="Photos")
    def photo_count(self, obj):
        return obj.images.count()

    @admin.display(description="Videos")
    def video_count(self, obj):
        return obj.videos.count()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # The cover can only be one of this album's own photos.
        if db_field.name == "cover_image":
            object_id = request.resolver_match.kwargs.get("object_id")
            if object_id:
                kwargs["queryset"] = GalleryImage.objects.filter(gallery_id=object_id)
            else:
                kwargs["queryset"] = GalleryImage.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # ----- Bulk upload (browser -> Cloudinary directly) -----

    def get_urls(self):
        custom = [
            path("<int:object_id>/bulk-upload/sign/",
                self.admin_site.admin_view(require_POST(self.bulk_upload_sign)),
                name="about_us_gallery_bulk_sign"),
            path("<int:object_id>/bulk-upload/save/",
                self.admin_site.admin_view(require_POST(self.bulk_upload_save)),
                name="about_us_gallery_bulk_save"),
        ]
        return custom + super().get_urls()

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        config = cloudinary.config()
        if str(object_id).isdigit():
            extra_context["bulk_upload"] = {
                "cloudName": config.cloud_name,
                "apiKey": config.api_key,
                "folder": gallery_upload_folder(object_id),
                "signUrl": reverse("admin:about_us_gallery_bulk_sign", args=[object_id]),
                "saveUrl": reverse("admin:about_us_gallery_bulk_save", args=[object_id]),
            }
        return super().change_view(request, object_id, form_url, extra_context)

    def _get_gallery_or_deny(self, request, object_id):
        gallery = self.get_object(request, str(object_id))
        if gallery is None:
            raise Http404
        if not self.has_change_permission(request, gallery):
            raise PermissionDenied
        return gallery

    @staticmethod
    def _json_body(request):
        try:
            data = json.loads(request.body or b"{}")
        except ValueError:
            return None
        return data if isinstance(data, dict) else None

    def bulk_upload_sign(self, request, object_id):
        """Sign the upload parameters so the API secret never reaches the browser."""
        gallery = self._get_gallery_or_deny(request, object_id)
        data = self._json_body(request)
        params = (data or {}).get("params_to_sign")
        if not isinstance(params, dict):
            return JsonResponse({"error": "Invalid request."}, status=400)
        # Only sign uploads that go into this album's own folder.
        if params.get("folder") != gallery_upload_folder(gallery.pk):
            return JsonResponse({"error": "Unexpected upload folder."}, status=400)
        signature = cloudinary.utils.api_sign_request(params, cloudinary.config().api_secret)
        return JsonResponse({"signature": signature})

    def bulk_upload_save(self, request, object_id):
        """Record files that the browser has already uploaded to Cloudinary."""
        gallery = self._get_gallery_or_deny(request, object_id)
        data = self._json_body(request)
        items = (data or {}).get("items")
        if not isinstance(items, list):
            return JsonResponse({"error": "Invalid request."}, status=400)

        prefix = gallery_upload_folder(gallery.pk) + "/"
        valid = []
        skipped = 0
        for item in items:
            if not isinstance(item, dict):
                skipped += 1
                continue
            public_id = str(item.get("public_id") or "")
            version = str(item.get("version") or "")
            resource_type = item.get("resource_type")
            file_format = item.get("format") or None
            signature = str(item.get("signature") or "")
            genuine = (
                resource_type in ("image", "video")
                and public_id.startswith(prefix)
                and version.isdigit()
                # Proves the file really was uploaded to our Cloudinary account.
                and cloudinary.utils.verify_api_response_signature(public_id, version, signature)
            )
            if not genuine:
                skipped += 1
                continue
            valid.append({
                "public_id": public_id, "version": version,
                "resource_type": resource_type, "format": file_format,
                "name": str(item.get("original_filename") or ""),
            })

        # Uploads finish in a random order; keep the albums in file-name order.
        valid.sort(key=lambda entry: entry["name"].lower())

        images, videos = [], []
        for entry in valid:
            resource = CloudinaryResource(
                public_id=entry["public_id"], version=entry["version"],
                format=entry["format"], type="upload",
                resource_type=entry["resource_type"],
            )
            if entry["resource_type"] == "image":
                if gallery.images.filter(image__contains=entry["public_id"]).exists():
                    continue
                images.append(GalleryImage(gallery=gallery, image=resource))
            else:
                if gallery.videos.filter(video__contains=entry["public_id"]).exists():
                    continue
                videos.append(GalleryVideo(gallery=gallery, video=resource))

        # Saved one by one so they keep distinct, increasing upload times.
        for obj in images + videos:
            obj.save()

        logger.info("Gallery %s: bulk upload saved %s images, %s videos, skipped %s",
                    gallery.pk, len(images), len(videos), skipped)
        return JsonResponse({"images": len(images), "videos": len(videos), "skipped": skipped})


# Register your models here.
admin.site.register(People)
