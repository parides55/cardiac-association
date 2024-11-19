from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Basket, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'stock', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'created_at', 'updated_at')
    list_editable = ('price', 'stock', 'available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('description',)


# Register your models here.
admin.site.register(Basket)
admin.site.register(Order)