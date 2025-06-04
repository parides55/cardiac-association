from django.contrib import admin
from .models import People
from django.contrib import admin
from .models import Gallery, GalleryImage, GalleryVideo


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1  # Allows adding multiple images at once
    

class GalleryVideoInline(admin.TabularInline):
    model = GalleryVideo
    extra = 1  # Allows adding multiple videos at once


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline, GalleryVideoInline]
    list_display = ("title", "created_at")


# Register your models here.
admin.site.register(People)