from django.contrib import admin
from .models import People
from django.contrib import admin
from .models import Gallery, GalleryImage


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1  # Allows adding multiple images at once


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    list_display = ("title", "created_at")


# Register your models here.
admin.site.register(People)
admin.site.register(GalleryImage)