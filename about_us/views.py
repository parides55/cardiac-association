from django.shortcuts import render
from django.contrib import messages
from django.views import generic
from .models import People

# Create your views here.

def our_history(request):
    return render(request, "about_us/history.html")

def our_people(request):

    try:
        board_members = People.objects.exclude(position=7).order_by('position')
        staff = People.objects.filter(position=7)

        context = {
            'board_members': board_members,
            'staff': staff
        }
        
        return render(request, "about_us/people.html", context) 
    
    except People.DoesNotExist:
        messages.info(request, "No board members or staff found.")
        return render(request, "about_us/people.html")

    except Exception as e:
        messages.error(request, f"The following error occurred: {e}")
        return render(request, "about_us/people.html")
