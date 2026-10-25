from django.shortcuts import render

from .models import Session


def home(request):
    """Home page: shows all study sessions, newest first."""
    # Get the sessions from the database. "-day" means newest date first.
    sessions = Session.objects.order_by("-day")
    # render() fills the template with our data and returns the finished page.
    # Each key in the dictionary becomes a variable name inside the template.
    return render(request, "tracker/home.html", {"sessions": sessions})


def about(request):
    """The about page: a simple page with no data from the database."""
    # No dictionary needed: this page doesn't show any data.
    return render(request, "tracker/about.html")
