from django.shortcuts import redirect, render

from .forms import SessionForm
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


def add_session(request):
    """Show the add-session form, and save it when the user submits it."""
    if request.method == "POST":
        # The user pressed Save: fill the form with what they typed.
        form = SessionForm(request.POST)
        if form.is_valid():  # Django checks every field (e.g. no negative minutes).
            form.save()  # Create the new session in the database.
            return redirect("home")  # Go to the home page to see the new session.
    else:
        # The user just opened the page: show an empty form.
        form = SessionForm()
    # We reach here when the page is first opened,
    # OR when the form had errors (it then shows the error messages).
    return render(request, "tracker/add_session.html", {"form": form})

