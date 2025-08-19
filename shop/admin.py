from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Basket, ShippingDetail, Donation


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    """
    Admin customization for the Product model.
    """
    list_display = ('name', 'price', 'stock', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'created_at', 'updated_at')
    list_editable = ('price', 'stock', 'available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('description',)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """
    Admin customization for the Basket model.
    """
    list_display = ('id', 'session_key', 'product', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('session_key', 'product__name')


class BasketInline(admin.TabularInline):
    """
    Inline admin for Basket items related to ShippingDetail.
    """
    model = ShippingDetail.basket_items.through  # Access the ManyToMany relationship through the intermediate table
    extra = 0  # No empty rows by default
    verbose_name = "Basket Item"
    verbose_name_plural = "Basket Items"


@admin.register(ShippingDetail)
class ShippingDetailAdmin(admin.ModelAdmin):
    """
    Admin customization for the ShippingDetail model.
    """
    list_display = ('id', 'full_name', 'email', 'phone_number', 'total_amount', 'created_at', 'get_basket_items')
    list_filter = ('created_at', 'city', 'area')
    search_fields = ('full_name', 'email', 'phone_number', 'address')
    inlines = [BasketInline]

    def get_basket_items(self, obj):
        """
        Custom method to display basket items in a readable format.
        """
        return ", ".join(
            [f"{item.product.name} (x{item.quantity})" for item in obj.basket_items.all()]
        )
    get_basket_items.short_description = 'Basket Items'  # Custom column name


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """
    Admin customization for the Donation model.
    """
    list_display = ('id', 'full_name', 'donation_amount', 'status', 'donation_type', 'created_at')
    list_filter = ('created_at', 'donation_type')
    search_fields = ('full_name', 'email', 'phone_number', 'address')