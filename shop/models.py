from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


#Online shop models
class Product(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = CloudinaryField('image', default='placeholder')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.name} - {self.stock} in stock'


    class Meta:
        ordering = ('-created_at',)


class Basket(models.Model):

    session_key = models.CharField(max_length=40)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Session {self.session_key} - {self.product.name} x {self.quantity}"


    class Meta:
        ordering = ('-created_at',)


class Order(models.Model):

    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)


    def __str__(self):
        return f'Order {self.id} for {self.full_name} - total amount: {self.total_amount}'


    class Meta:
        ordering = ('-created_at',)


#Donation models
class Donation(models.Model):
    
    DONATION_TYPE_CHOICES = [
        ('one-off', 'One-Off Payment'),
        ('monthly', 'Monthly Subscription'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.full_name} / {self.donation_type} / {self.donation_amount} - {self.status}'
    
    
    class Meta:
        ordering = ('-created_at',)