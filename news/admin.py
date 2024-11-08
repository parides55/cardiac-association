from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import New


@admin.register(New)
class EventAdmin(SummernoteModelAdmin):

    list_display = ('title', 'created_on', 'status')
    list_filter = ('created_on', 'status')
    search_fields = ['title', 'created_on']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
# Register your models here.