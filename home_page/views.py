from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. HOME PAGE of  The cardiac association here!")