from django.shortcuts import render


def index(request):
    return render(request, "home_page/index.html")

def MoreInfo(request):
    return render(request, "home_page/heart_disease_info.html")