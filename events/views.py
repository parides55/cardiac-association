from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from .models import Event

# Create your views here.
def events(request):

    today = datetime.now()
    current_month = datetime.now().month
    current_year = datetime.now().year

    try:
        queryset = Event.objects.filter(status=1)

        current_month_events = queryset.filter(
            date_of_event__month=current_month,
            date_of_event__year=current_year,
            ).order_by('date_of_event')

        upcoming_events = queryset.filter(
            date_of_event__gt=today,
        ).exclude(
            date_of_event__month=current_month,
            date_of_event__year=current_year
        ).order_by('date_of_event')

        past_events = queryset.filter(
            date_of_event__lt=today,
        ).order_by('-date_of_event') 

        context = {
            'current_month_events': current_month_events,
            'upcoming_events': upcoming_events,
            'past_events': past_events,
        }

        return render(request, "events/events.html", context)

    except Event.DoesNotExist:
        messages.info(request, "Events not found.")
        return redirect('events')

    except Exception as e:
        messages.error(request, f"The following error occurred: {str(e)}")
        return redirect('events')


def event_info(request, slug):

    try:
        queryset_info = Event.objects.filter(status=1)
        event = get_object_or_404(queryset_info, slug=slug)

        context = {
            'event': event,
        }

        return render(request, "events/event_info.html", context)

    except Event.DoesNotExist:
        messages.info(request, 'Event not found.')
        return redirect('events')

    except Exception as e:
        messages.error(request, f"The following error occurred: {str(e)}")
        return redirect('events')