from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Member


@admin.register(Member)
class MemberAdmin(SummernoteModelAdmin):
    
    list_display = ('id', 'name', 'surname', 'date_of_birth', 'created_at')
    list_filter = ('date_of_birth', 'name', 'surname',)
    search_fields = ['name', 'surname', 'email', 'id_number', 'date_of_birth']

# Register your models here.
