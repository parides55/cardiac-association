from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from .forms import MemberForm


def index(request):
    return render(request, "home_page/index.html")

def MoreInfo(request):
    return render(request, "home_page/heart_disease_info.html")

def Become_member(request):
    
    try:
        if request.method == 'POST':
            member_form = MemberForm(request.POST)
            if member_form.is_valid():
                member_form.save()
                messages.success(
                    request,
                    "You have been successfully registered as a member and we will be in touch with you soon."
                )
                return redirect('become_member')
            else:
                messages.error(
                    request,
                    "There has been error processing your request. Please try completing the form again."
                )
        member_form = MemberForm()
        return render(
            request, "home_page/become_member.html",
            {'member_form': member_form}
        )
    except Exception as e:
        messages.error(request, f"The following error occurred: {str(e)}")
        return redirect('become_member')

def Donations(request):
    return render(request, "home_page/donations.html")