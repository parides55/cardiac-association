from django.shortcuts import render

# Create your views here.
def WhatWeDo(request):
    return render(request, "what_we_do/what_we_do.html")

def Services(request):
    return render(request, "what_we_do/services.html")

def Programs(request):
    return render(request, "what_we_do/programs.html")