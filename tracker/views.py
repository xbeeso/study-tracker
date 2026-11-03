from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count, IntegerField, Q, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from .forms import SessionForm, SignupForm

from .models import Course, Session


@login_required
def home(request):
    """Main page: only the logged-in user's sessions, newest first."""
    # filter(user=request.user) is the most important part: without it, everyone sees everything.
    sessions = Session.objects.filter(user=request.user).order_by("-day")
    return render(request, "tracker/home.html", {"sessions": sessions})

def about(request):
    """The about page: a simple page with no data from the database."""
    # No dictionary needed: this page doesn't show any data.
    return render(request, "tracker/about.html")

@login_required  # A guard: visitors who aren't logged in get sent to the login page.
def add_session(request):
    """Show the add-session form, and save it when the user submits it."""
    if request.method == "POST":
        # The user pressed Save: fill the form with what they typed.
        form = SessionForm(request.POST)
        if form.is_valid():  # Django checks every field (e.g. no negative minutes).
             # commit=False: build the session object, but don't save it to the database yet.
            session = form.save(commit=False)
            # The owner comes from who is logged in, NEVER from the form.
            session.user = request.user
            session.save()
            return redirect("home")  # Go to the home page to see the new session.
    else:
        # The user just opened the page: show an empty form.
        form = SessionForm()
    # The same template is used for adding AND editing, so we send the page title too.
        return render(request, "tracker/add_session.html", {"form": form, "title": "إضافة جلسة مذاكرة"})


@login_required
def course_list(request):
    """All courses, each with how many sessions the logged-in user studied in it."""
    courses = Course.objects.annotate(
        # filter=Q(...): count only the sessions that belong to the logged-in user.
        session_count=Count("sessions", filter=Q(sessions__user=request.user))
    ).order_by("name")
    return render(request, "tracker/course_list.html", {"courses": courses})

@login_required
def course_detail(request, pk):
    """One course's page: its sessions and its total time."""
    # Find the course with this number. If it doesn't exist, show a 404 page instead of crashing.
    course = get_object_or_404(Course, pk=pk)
    # Only THIS course's sessions (thanks to related_name="sessions" in models.py).
        # Only YOUR sessions in this course, not everyone's.
    sessions = course.sessions.filter(user=request.user).order_by("-day")
    # Add up all the minutes. "or 0": if there are no sessions, Sum gives None (nothing).
    total_minutes = sessions.aggregate(total=Sum("minutes"))["total"] or 0
    return render(request, "tracker/course_detail.html", {
        "course": course,
        "sessions": sessions,
        "total_minutes": total_minutes,
    })


@login_required
def edit_session(request, pk):
    """Edit one of YOUR sessions. Someone else's session number gives 404."""
    # pk alone means "any session with this number".
    # Adding user=request.user means "...and it must be mine". This one condition stops IDOR.
    session = get_object_or_404(Session, pk=pk, user=request.user)
    if request.method == "POST":
        # instance=session: update this existing session instead of creating a new one.
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            # Safe: "user" is not in the form's fields, so the owner can't be changed here.
            form.save()
            return redirect("home")
    else:
        form = SessionForm(instance=session)
    return render(request, "tracker/add_session.html", {"form": form, "title": "تعديل الجلسة"})


@login_required
def delete_session(request, pk):
    """Delete one of YOUR sessions: GET shows a confirm page, POST deletes."""
    # Same ownership check as edit: you can only delete what's yours.
    session = get_object_or_404(Session, pk=pk, user=request.user)
    if request.method == "POST":
        session.delete()
        return redirect("home")
    return render(request, "tracker/session_confirm_delete.html", {"session": session})

@login_required
def stats(request):
    """Statistics page: total hours, this week's hours, and hours per course (for the logged-in user)."""
    # Start from YOUR sessions only. Every number below is built on top of this.
    my_sessions = Session.objects.filter(user=request.user)

    total_minutes = my_sessions.aggregate(total=Sum("minutes"))["total"] or 0

    # The Saudi week starts on Sunday. weekday(): Monday=0 ... Sunday=6.
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    week_start = today - timedelta(days=days_since_sunday)
    week_minutes = my_sessions.filter(day__gte=week_start).aggregate(total=Sum("minutes"))["total"] or 0

    # Minutes per course, counting only YOUR sessions. Coalesce turns "no sessions" (None) into 0.
    courses = list(
        Course.objects.annotate(
            total_minutes=Coalesce(
                Sum("sessions__minutes", filter=Q(sessions__user=request.user)),
                0,
                output_field=IntegerField(),
            )
        ).order_by("-total_minutes")
    )

    for course in courses:
        course.hours = round(course.total_minutes / 60, 1)
        # Progress toward the target, as a whole-number percentage (0 to 100).
        if course.target_hours > 0:
            course.percent = min(round(course.total_minutes / (course.target_hours * 60) * 100), 100)
        else:
            # A target of 0 would mean dividing by zero.
            course.percent = 0

    # The list is sorted biggest first, so the top course is the first one (if any).
    top_course = courses[0] if courses else None

    return render(request, "tracker/stats.html", {
        "total_hours": round(total_minutes / 60, 1),
        "week_hours": round(week_minutes / 60, 1),
        "top_course": top_course,
        "courses": courses,
    })

def signup(request):
    """Create a new account, then log the user in right away."""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # save() stores the password HASHED, never as plain text.
            user = form.save()
            # Log them in now, so they don't have to type the password again.
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


