from datetime import date, timedelta

from django.db.models import Count, IntegerField, Sum
from django.db.models.functions import Coalesce
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


def stats(request):
    """Statistics page: total hours, this week's hours, and hours per course."""
    # 1) Total minutes of ALL sessions. Same as yesterday's: SELECT SUM(minutes)
    total_minutes = Session.objects.aggregate(total=Sum("minutes"))["total"] or 0

    # 2) This week, starting from Sunday (the Saudi week).
    today = date.today()
    # weekday(): Monday=0 ... Sunday=6. This gives how many days have passed since Sunday.
    days_since_sunday = (today.weekday() + 1) % 7
    week_start = today - timedelta(days=days_since_sunday)
    # day__gte = "day is greater than or equal to". Same as: WHERE day >= week_start
    week_minutes = Session.objects.filter(day__gte=week_start).aggregate(total=Sum("minutes"))["total"] or 0

    # 3) Every course with its total minutes, biggest first.
    # Same as yesterday's LEFT JOIN + GROUP BY + ORDER BY. Coalesce = COALESCE: no sessions -> 0.
    courses = list(
        Course.objects.annotate(
            total_minutes=Coalesce(Sum("sessions__minutes"), 0, output_field=IntegerField())
        ).order_by("-total_minutes")
    )
    # Loop over the courses and give each one its hours (templates can't divide numbers).
    for course in courses:
        course.hours = round(course.total_minutes / 60, 1)
        # Progress toward the target, as a whole-number percentage (0 to 100).
        if course.target_hours > 0:
            # target_hours * 60 turns the target into minutes, so both sides use the same unit.
            # min(..., 100) stops the bar from going past 100% if you study more than the target.
            course.percent = min(round(course.total_minutes / (course.target_hours * 60) * 100), 100)
        else:
            # A target of 0 would mean dividing by zero, which crashes Python.
            course.percent = 0

    # The top course is the first one, or None if there are no courses at all.
    top_course = courses[0] if courses else None

    return render(request, "tracker/stats.html", {
        "total_hours": round(total_minutes / 60, 1),
        "week_hours": round(week_minutes / 60, 1),
        "top_course": top_course,
        "courses": courses,
    })


