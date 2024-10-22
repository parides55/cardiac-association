from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import HeroImage

@admin.register(HeroImage)
class HeroImageAdmin(SummernoteModelAdmin):

    list_display = ('title', 'created_on', 'active')
    list_filter = ('created_on', 'active')
    search_fields = ['title', 'created_on']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)


# Register your models here.