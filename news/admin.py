from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import New


@admin.register(New)
class EventAdmin(SummernoteModelAdmin):

    list_display = ('title_greek', 'created_on', 'status')
    list_filter = ('created_on', 'status')
    search_fields = ['title_english', 'created_on']
    prepopulated_fields = {'slug': ('title_english',)}
    summernote_fields = ('content_english', 'content_greek')
# Register your models here.