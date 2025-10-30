from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Event


@admin.register(Event)
class EventAdmin(SummernoteModelAdmin):

    list_display = ('title_greek', 'created_on', 'date_of_event', 'status')
    list_filter = ('created_on', 'status')
    search_fields = ['title_greek', 'created_on']
    prepopulated_fields = {'slug': ('title_english',)}
    summernote_fields = ('content_english', 'content_greek')

# Register your models here.
