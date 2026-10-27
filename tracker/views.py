from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SessionForm
from .models import Course, Session


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
    # The same template is used for adding AND editing, so we send the page title too.
        return render(request, "tracker/add_session.html", {"form": form, "title": "إضافة جلسة مذاكرة"})


def course_list(request):
    """Courses page: every course with how many sessions it has."""
    # annotate() adds a new value to each course: the number of its sessions.
    # It's our sessions_count() loop from day 2, done by the database for every course.
    courses = Course.objects.annotate(session_count=Count("sessions")).order_by("name")
    return render(request, "tracker/course_list.html", {"courses": courses})


def course_detail(request, pk):
    """One course's page: its sessions and its total time."""
    # Find the course with this number. If it doesn't exist, show a 404 page instead of crashing.
    course = get_object_or_404(Course, pk=pk)
    # Only THIS course's sessions (thanks to related_name="sessions" in models.py).
    sessions = course.sessions.order_by("-day")
    # Add up all the minutes. "or 0": if there are no sessions, Sum gives None (nothing).
    total_minutes = sessions.aggregate(total=Sum("minutes"))["total"] or 0
    return render(request, "tracker/course_detail.html", {
        "course": course,
        "sessions": sessions,
        "total_minutes": total_minutes,
    })


def edit_session(request, pk):
    """Edit an existing session: the same form as 'add', but filled with its current data."""
    # Find the session by its number, or show a 404 page.
    session = get_object_or_404(Session, pk=pk)
    if request.method == "POST":
        # instance=session: UPDATE this session instead of creating a new one.
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        # Show the form already filled with the session's current values.
        form = SessionForm(instance=session)
    # Reuse the add-session template, with a different title.
        return render(request, "tracker/add_session.html", {"form": form, "title": "تعديل الجلسة"})


def delete_session(request, pk):
    """Ask for confirmation first, then delete the session."""
    session = get_object_or_404(Session, pk=pk)
    if request.method == "POST":
        # The user pressed "Yes, delete" in the confirmation form.
        session.delete()
        return redirect("home")
    # First visit: show the confirmation page.
    return render(request, "tracker/session_confirm_delete.html", {"session": session})