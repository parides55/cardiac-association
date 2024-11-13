from django.shortcuts import render


def index(request):
    return render(request, "home_page/index.html")

def MoreInfo(request):
    return render(request, "home_page/heart_disease_info.html")

def Become_member(request):
    return render(request, "home_page/become_member.html")

def Donations(request):
    return render(request, "home_page/donations.html")