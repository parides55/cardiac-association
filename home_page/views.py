from django.shortcuts import render
from .forms import ContactForm


def index(request):
    return render(request, "home_page/index.html")

def MoreInfo(request):
    return render(request, "home_page/heart_disease_info.html")

def Become_member(request):
    comment_form = ContactForm()
    return render(request,
                "home_page/become_member.html"
                , {'comment_form': comment_form})

def Donations(request):
    return render(request, "home_page/donations.html")