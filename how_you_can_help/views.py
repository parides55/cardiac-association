from django.shortcuts import render

# Create your views here.
def HowYouCanHelp(request):
    return render(request, "how_you_can_help/how_you_can_help.html")