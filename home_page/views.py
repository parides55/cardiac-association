from django.shortcuts import render
from .forms import MemberForm


def index(request):
    return render(request, "home_page/index.html")

def MoreInfo(request):
    return render(request, "home_page/heart_disease_info.html")

def Become_member(request):
    member_form = MemberForm()
    return render(request,
                "home_page/become_member.html"
                , {'member_form': member_form})

def Donations(request):
    return render(request, "home_page/donations.html")