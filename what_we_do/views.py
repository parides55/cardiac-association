from django.shortcuts import render

# Create your views here.
def WhatWeDo(request):
    return render(request, "what_we_do/what_we_do.html")