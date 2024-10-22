from django.contrib import admin
from .models import HeroImage

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):

    list_display = ['title', 'created_on', 'active']
    list_filter = ['created_on', 'active']
    search_fields = ['title', 'created_on']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)


# Register your models here.