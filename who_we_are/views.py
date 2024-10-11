from django.shortcuts import render

# Create your views here.
def who_we_are(request):
    return render(request, "who_we_are/who_we_are.html")