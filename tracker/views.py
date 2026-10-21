# HttpResponse: sends simple text back to the browser.
from django.http import HttpResponse


def home(request):
    """The home page: Django calls this when someone opens the site's main address."""
    # request = everything the browser sent us (we don't use it yet).
    return HttpResponse("Welcome to Study Tracker")


def about(request):
    """The about page: explains what this project is."""
    return HttpResponse("Study Tracker helps you log your study sessions and track your progress.")

