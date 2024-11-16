from django.shortcuts import render
from datetime import datetime
from .models import Event

# Create your views here.
def events(request):
    today = datetime.now()
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    current_month_events = Event.objects.filter(
        date_of_event__month=current_month,
        date_of_event__year=current_year,
        status=1
        ).order_by('date_of_event')
    
    upcoming_events = Event.objects.filter(
        date_of_event__gt=today,
        status=1
    ).exclude(
        date_of_event__month=current_month,
        date_of_event__year=current_year
    ).order_by('date_of_event')
    
    past_events = Event.objects.filter(
        date_of_event__lt=today,
        status=1
    ).order_by('-date_of_event') 
    
    context = {
        'current_month_events': current_month_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    
    return render(request, "events/events.html", context)