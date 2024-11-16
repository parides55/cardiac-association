from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from .models import New

# Create your views here.
class News(generic.ListView):
    
    queryset = New.objects.filter(status=1).order_by('-created_on')
    template_name = "news/news.html"
    paginate_by = 6


def new_detail(request, slug):

    try:
        queryset = New.objects.filter(status=1)
        new = get_object_or_404(queryset, slug=slug)

        context = {
            'new': new,
        }

        return render(request, "news/new_details.html", context)

    except New.DoesNotExist:
        messages.info(request, 'News not found.')
        return redirect('events')

    except Exception as e:
        messages.error(request, f"The following error occurred: {str(e)}")
        return redirect('events')