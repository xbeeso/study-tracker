# Import the date tool so we can get today's date automatically.
from datetime import date


class StudySession:
    """One study session: which course, how long, a short note, and the date."""

    def __init__(self, course, minutes, note="", day=None):
        # Runs automatically when we create a new session.
        # It saves the session's details inside the object (self).
        self.course = course
        self.minutes = minutes
        self.note = note  # Optional: empty text if we don't give one.
        # Use the given date if there is one, otherwise use today's date.
        self.day = day if day else date.today()

    def __str__(self):
        # Controls how a session looks when we print it.
        # Without this, print() shows a strange memory address instead.
        return f"{self.day} | {self.course} | {self.minutes} min | {self.note}"


def total_hours(sessions):
    """Return the total study hours for ALL sessions."""
    total_minutes = 0  # Start the counter BEFORE the loop so it keeps its value.
    for session in sessions:  # Go through the sessions one by one.
        total_minutes += session.minutes  # Add this session's minutes.
    # AFTER the loop ends: convert minutes to hours, keep 1 decimal place.
    return round(total_minutes / 60, 1)


def hours_for_course(sessions, course_name):
    """Return the study hours for ONE course only."""
    total_minutes = 0
    for session in sessions:
        # Filter: only count sessions that belong to the requested course.
        if session.course == course_name:
            total_minutes += session.minutes  # Inside the if: runs only when it matches.
    return round(total_minutes / 60, 1)


def sessions_count(sessions, course_name):
    """Return how many sessions we studied for ONE course."""
    total_sessions = 0
    for session in sessions:
        if session.course == course_name:
            total_sessions += 1  # Count the session (add 1), not its minutes.
    return total_sessions  # No division here: we want a count, not hours.


# ---- Test data: a list of sessions made from the StudySession class ----
sessions = [
    StudySession("Python 101", 90, "loops"),
    StudySession("SQL 101", 60, "SELECT"),
    StudySession("Python 101", 30, "functions"),
]

# ---- Try the functions ----
for session in sessions:
    print(session)  # Uses __str__ to print each session nicely.

print("Total hours:", total_hours(sessions))  # Expected: 3.0
print("Python 101 hours:", hours_for_course(sessions, "Python 101"))  # Expected: 2.0
print("Python 101 sessions:", sessions_count(sessions, "Python 101"))  # Expected: 2
