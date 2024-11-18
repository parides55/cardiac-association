from django.shortcuts import render

# Create your views here.
def Donations(request):
    return render(request, "shop/donations.html")

def OnlineShop(request):
    return render(request, "shop/online_shop.html")