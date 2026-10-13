from django.db import models
from cloudinary import CloudinaryResource
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _


# Create your models here.
POSITIONS = (
    (0, _("President")), (1, _("Vice President")), (2, _("Secretary")), (3, _("Assistant Secretary")),
            (4, _("Treasurer")), (5, _("Assistant Treasurer")), (6, _("Member")), (7, _("Executive Director")), (8, _("Liaison Officer"))
)


class People(models.Model):

    name_en = models.CharField(max_length=100)
    name_gr = models.CharField(max_length=100)
    image = CloudinaryField('image', default='placeholder')
    position = models.IntegerField(choices=POSITIONS, default=0)

    def __str__(self):
        return f"{self.name_en} - {self.get_position_display()}"


# Sizes used across the gallery. Cloudinary generates (and caches) each
# variant on first request, so the browser never downloads an original.
GALLERY_THUMB = dict(width=600, height=450, crop="fill", gravity="auto",
                    quality="auto", fetch_format="auto")
GALLERY_COVER = dict(width=800, height=600, crop="fill", gravity="auto",
                    quality="auto", fetch_format="auto")
GALLERY_LARGE = dict(width=1600, height=1600, crop="limit",
                    quality="auto", fetch_format="auto")


def _as_resource(value, resource_type="image"):
    """Accept a CloudinaryResource or the raw string stored in the database."""
    if not value:
        return None
    if isinstance(value, CloudinaryResource):
        return value
    return CloudinaryField(resource_type=resource_type).parse_cloudinary_resource(value)


def image_url(value, **options):
    resource = _as_resource(value, "image")
    return resource.build_url(**options) if resource else ""


def video_poster_url(value, **options):
    """A JPEG frame from the video, used as its thumbnail."""
    resource = _as_resource(value, "video")
    if not resource:
        return ""
    return resource.build_url(resource_type="video", format="jpg",
                              start_offset="auto", **options)


class Gallery(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ForeignKey(
        "GalleryImage", on_delete=models.SET_NULL, blank=True, null=True,
        related_name="+",
        help_text="Shown on the album card. If empty, the first photo is used.",
    )
    order = models.PositiveIntegerField(
        default=0, db_index=True,
        help_text="Lower numbers appear first. Albums with the same number are shown newest first.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name_plural = "Galleries"

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image')
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "uploaded_at", "id"]

    def __str__(self):
        return self.caption or f"Image {self.pk} in {self.gallery.title}"

    @property
    def thumb_url(self):
        return image_url(self.image, **GALLERY_THUMB)

    @property
    def large_url(self):
        return image_url(self.image, **GALLERY_LARGE)


class GalleryVideo(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="videos")
    video = CloudinaryField('video', resource_type='video')
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "uploaded_at", "id"]

    def __str__(self):
        return self.caption or f"Video {self.pk} in {self.gallery.title}"

    @property
    def poster_url(self):
        return video_poster_url(self.video, **GALLERY_THUMB)
