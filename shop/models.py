from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator

# Create your models here.


#Online shop models
class Product(models.Model):

    name = models.CharField(max_length=100, verbose_name="Product Name")
    slug = models.SlugField(max_length=100, unique=True)
    image = CloudinaryField('image', default='placeholder')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (€)")
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def is_available(self):
        return self.available and self.stock > 0

    def __str__(self):
        return f'{self.name} - {self.stock} in stock'


    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]


class Basket(models.Model):

    session_key = models.CharField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Session {self.session_key} - {self.product.name} x {self.quantity}"


    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(fields=['session_key', 'product'], name='unique_basket_item')
        ]


class ShippingDetail(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField(max_length=250)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    basket_items = models.ManyToManyField(Basket, related_name='shipping_items')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Order {self.id} for {self.full_name} - total amount: {self.total_amount}'


    class Meta:
        ordering = ('-created_at',)


#Donation models
class Donation(models.Model):
    
    DONATION_TYPE_CHOICES = [
        ('One-Off Payment', 'One-Off Payment'),
        ('Monthly Subscription', 'Monthly Subscription'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('one-off', 'One-Off'),
    ]
    
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField(max_length=250)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.full_name} donated €{self.donation_amount} on {self.created_at} - {self.status}'
    
    
    class Meta:
        ordering = ('-created_at',)