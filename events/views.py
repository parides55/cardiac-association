from django.shortcuts import render
from datetime import datetime
from .models import Event

# Create your views here.
def events(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    current_month_events = Event.objects.filter(
        date_of_event__month=current_month,
        date_of_event__year=current_year,
        status=1
        )
    
    past_events = Event.objects.exclude(
        date_of_event__month=current_month,
        date_of_event__year=current_year,
        status=0
    )
    
    context = {
        'current_month_events': current_month_events,
        'past_events': past_events,
    }
    
    return render(request, "events/events.html", context)