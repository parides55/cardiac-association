from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import New

# Create your views here.
class News(generic.ListView):
    
    queryset = New.objects.filter(status=1).order_by('-created_on')
    template_name = "news/news.html"
    paginate_by = 6