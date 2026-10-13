import json

import cloudinary
import cloudinary.utils
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from .models import Gallery, GalleryImage, GalleryVideo


def response_signature(public_id, version):
    """The signature Cloudinary attaches to a genuine upload response."""
    return cloudinary.utils.api_sign_request(
        {"public_id": public_id, "version": version}, cloudinary.config().api_secret)


class GalleryPagesTests(TestCase):

    def setUp(self):
        translation.activate("en")  # URLs are language-prefixed
        self.album = Gallery.objects.create(title="Summer camp", description="Fun")
        self.image = GalleryImage.objects.create(
            gallery=self.album, image="image/upload/v1/gallery/1/photo.jpg", caption="Kids")
        self.video = GalleryVideo.objects.create(
            gallery=self.album, video="video/upload/v1/gallery/1/clip.mp4")

    def test_album_list_shows_resized_cover_not_original(self):
        response = self.client.get(reverse("gallery_view"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Summer camp")
        self.assertContains(response, reverse("gallery_detail", args=[self.album.pk]))
        self.assertContains(response, "c_fill")
        self.assertContains(response, 'loading="lazy"')

    def test_empty_album_is_hidden_from_list(self):
        Gallery.objects.create(title="Not ready yet")
        response = self.client.get(reverse("gallery_view"))
        self.assertNotContains(response, "Not ready yet")

    def test_chosen_cover_is_used(self):
        other = GalleryImage.objects.create(
            gallery=self.album, image="image/upload/v1/gallery/1/chosen.jpg")
        self.album.cover_image = other
        self.album.save()
        response = self.client.get(reverse("gallery_view"))
        self.assertContains(response, "gallery/1/chosen")
        self.assertNotContains(response, "gallery/1/photo")

    def test_video_only_album_uses_video_frame_as_cover(self):
        album = Gallery.objects.create(title="Concert")
        GalleryVideo.objects.create(gallery=album, video="video/upload/v1/gallery/9/show.mp4")
        response = self.client.get(reverse("gallery_view"))
        self.assertContains(response, "gallery/9/show.jpg")

    def test_list_query_count_does_not_grow_with_albums(self):
        for number in range(5):
            album = Gallery.objects.create(title=f"Album {number}")
            GalleryImage.objects.create(gallery=album, image=f"image/upload/v1/a/{number}.jpg")
        with self.assertNumQueries(2):  # count for pagination + the albums
            self.client.get(reverse("gallery_view"))

    def test_album_page_uses_thumbnails_and_video_poster(self):
        response = self.client.get(reverse("gallery_detail", args=[self.album.pk]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn("w_600", html)      # grid thumbnail
        self.assertIn("w_1600", html)     # lightbox version
        self.assertIn("gallery/1/clip.jpg", html)   # poster frame
        self.assertIn("gallery/1/clip.mp4", html)   # the video itself
        self.assertIn("Kids", html)

    def test_unknown_album_is_404(self):
        response = self.client.get(reverse("gallery_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)


class GalleryBulkUploadTests(TestCase):

    def setUp(self):
        translation.activate("en")  # URLs are language-prefixed
        self.album = Gallery.objects.create(title="Gala")
        self.folder = f"gallery/{self.album.pk}"
        self.admin = get_user_model().objects.create_superuser("admin", "a@b.c", "pw")
        self.sign_url = reverse("admin:about_us_gallery_bulk_sign", args=[self.album.pk])
        self.save_url = reverse("admin:about_us_gallery_bulk_save", args=[self.album.pk])

    def post(self, url, payload):
        return self.client.post(url, json.dumps(payload), content_type="application/json")

    def item(self, name, resource_type="image", file_format="jpg", **extra):
        public_id = f"{self.folder}/{name}"
        data = {
            "public_id": public_id, "version": 1700000000,
            "signature": response_signature(public_id, 1700000000),
            "resource_type": resource_type, "format": file_format,
            "original_filename": name,
        }
        data.update(extra)
        return data

    def test_endpoints_require_staff_login(self):
        for url in (self.sign_url, self.save_url):
            response = self.post(url, {})
            self.assertEqual(response.status_code, 302)
            self.assertIn("login", response["Location"])
        self.assertEqual(GalleryImage.objects.count(), 0)

    def test_non_staff_user_is_rejected(self):
        get_user_model().objects.create_user("visitor", "v@b.c", "pw")
        self.client.login(username="visitor", password="pw")
        response = self.post(self.save_url, {"items": [self.item("a")]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(GalleryImage.objects.count(), 0)

    def test_sign_returns_valid_signature_for_album_folder(self):
        self.client.force_login(self.admin)
        params = {"folder": self.folder, "timestamp": 1700000000, "source": "uw"}
        response = self.post(self.sign_url, {"params_to_sign": params})
        self.assertEqual(response.status_code, 200)
        expected = cloudinary.utils.api_sign_request(params, cloudinary.config().api_secret)
        self.assertEqual(response.json()["signature"], expected)

    def test_sign_refuses_other_folders(self):
        self.client.force_login(self.admin)
        response = self.post(self.sign_url, {"params_to_sign": {"folder": "somewhere/else", "timestamp": 1}})
        self.assertEqual(response.status_code, 400)

    def test_save_creates_images_and_videos_in_filename_order(self):
        self.client.force_login(self.admin)
        items = [self.item("IMG_002"), self.item("clip", "video", "mp4"), self.item("IMG_001")]
        response = self.post(self.save_url, {"items": items})
        self.assertEqual(response.json(), {"images": 2, "videos": 1, "skipped": 0})

        images = list(self.album.images.all())
        self.assertEqual([i.image.public_id for i in images],
                         [f"{self.folder}/IMG_001", f"{self.folder}/IMG_002"])
        self.assertIn(f"/image/upload/v1700000000/{self.folder}/IMG_001.jpg", images[0].image.url)
        video = self.album.videos.get()
        self.assertEqual(video.video.resource_type, "video")
        self.assertIn(f"/video/upload/v1700000000/{self.folder}/clip.mp4", video.video.url)

    def test_save_skips_forged_foreign_and_duplicate_files(self):
        self.client.force_login(self.admin)
        forged = self.item("forged", signature="0" * 40)
        outside = {"public_id": "other/x", "version": 1, "resource_type": "image", "format": "jpg",
                   "signature": response_signature("other/x", 1)}
        raw = self.item("doc", "raw", "pdf")
        good = self.item("good")
        response = self.post(self.save_url, {"items": [forged, outside, raw, good, "junk"]})
        self.assertEqual(response.json(), {"images": 1, "videos": 0, "skipped": 4})

        # Sending the same file again must not create a second row.
        response = self.post(self.save_url, {"items": [good]})
        self.assertEqual(response.json()["images"], 0)
        self.assertEqual(self.album.images.count(), 1)

    def test_bad_payloads_and_get_are_rejected(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.post(self.save_url, {"items": "nope"}).status_code, 400)
        self.assertEqual(self.client.post(self.save_url, "not json", content_type="application/json").status_code, 400)
        self.assertEqual(self.client.get(self.save_url).status_code, 405)

    def test_change_page_shows_upload_button_and_add_page_does_not(self):
        self.client.force_login(self.admin)
        change = self.client.get(reverse("admin:about_us_gallery_change", args=[self.album.pk]))
        self.assertContains(change, "bulk-upload-button")
        self.assertContains(change, "gallery_bulk_upload.js")
        add = self.client.get(reverse("admin:about_us_gallery_add"))
        self.assertEqual(add.status_code, 200)
        self.assertNotContains(add, "bulk-upload-button")

    def test_cover_choices_are_limited_to_this_album(self):
        mine = GalleryImage.objects.create(gallery=self.album, image="image/upload/v1/mine.jpg")
        other_album = Gallery.objects.create(title="Other")
        theirs = GalleryImage.objects.create(gallery=other_album, image="image/upload/v1/theirs.jpg")
        self.client.force_login(self.admin)
        response = self.client.get(reverse("admin:about_us_gallery_change", args=[self.album.pk]))
        choices = response.context["adminform"].form.fields["cover_image"].queryset
        self.assertIn(mine, choices)
        self.assertNotIn(theirs, choices)
