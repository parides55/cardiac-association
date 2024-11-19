from django.shortcuts import render
from .models import Product

# Create your views here.
def Donations(request):
    return render(request, "shop/donations.html")

def OnlineShop(request):

    products = Product.objects.filter(available=True).order_by('-created_at')
    
    context = {
        'products': products,
    }
    return render(request, "shop/online_shop.html", context)