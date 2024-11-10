from django.shortcuts import render

# Create your views here.

def our_history(request):
    return render(request, "about_us/history.html")

def our_people(request):
    return render(request, "about_us/people.html")