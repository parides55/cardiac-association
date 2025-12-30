from django.db import models
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


class Gallery(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image')
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image in {self.gallery.title}"

class GalleryVideo(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="videos")
    video = CloudinaryField('video', resource_type='video')
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video in {self.gallery.title}"
