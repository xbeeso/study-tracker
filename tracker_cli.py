# json: saves Python data to a file and reads it back.
import json
# Import the date tool so we can get today's date automatically.
from datetime import date

# The file where all sessions are saved. Written once here,
# so if we want to rename it later, we change one line only.
DATA_FILE = "sessions.json"

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


def ask_minutes():
    """Ask the user for minutes until they type a valid positive number."""
    while True:  # Keep asking forever... until we return.
        text = input("Minutes: ")  # input() always gives us text, not a number.
        # Valid only if it has digits only AND is bigger than zero.
        if text.isdigit() and int(text) > 0:
            return int(text)  # Convert to a number and exit the function (and the loop).
        # We only reach this line if the input was wrong.
        print("Please enter a positive number.")


def summary_by_course(sessions):
    """Return a dictionary: each course name -> its total minutes."""
    totals = {}  # Empty dictionary: like a two-column table (course | minutes).
    for session in sessions:
        if session.course in totals:
            # Seen this course before: add to its existing total.
            totals[session.course] += session.minutes
        else:
            # First time we see this course: create a new row for it.
            totals[session.course] = session.minutes
    return totals



def save_sessions(sessions):
    """Save all sessions to the JSON file."""
    data = []  # JSON can't store our class, so we build a list of plain dictionaries.
    for session in sessions:
        data.append({
            "course": session.course,
            "minutes": session.minutes,
            "note": session.note,
            "day": session.day.isoformat(),  # Date -> text like "2026-10-20".
        })
    # "w" = write mode: replaces the old file content with the new data.
    # "with" closes the file automatically when we finish.
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        # ensure_ascii=False keeps Arabic text readable. indent=2 makes it tidy.
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_sessions():
    """Read sessions from the JSON file and turn them back into StudySession objects."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:  # "r" = read mode.
            data = json.load(f)
    except FileNotFoundError:
        # First run: the file doesn't exist yet, so start with an empty list.
        return []

    sessions = []
    for item in data:  # The mirror of save_sessions: dictionary -> object.
        day = date.fromisoformat(item["day"])  # Text -> date.
        sessions.append(StudySession(item["course"], item["minutes"], item["note"], day))
    return sessions


def add_session(sessions):
    """Ask the user for a new session, add it to the list, and save."""
    course = input("Course: ")
    minutes = ask_minutes()  # Reuse our safe question instead of plain input().
    note = input("Note (optional): ")
    sessions.append(StudySession(course, minutes, note))  # Build a session from the class.
    save_sessions(sessions)  # Save right away so nothing is lost.
    print("Saved!")


def show_summary(sessions):
    """Print the total hours for every course."""
    totals = summary_by_course(sessions)  # Reuse: get {course: minutes}.
    for course, minutes in totals.items():  # .items() gives each (name, minutes) pair.
        print(f"{course}: {round(minutes / 60, 1)} hours")


def main():
    """The main menu: shows options and sends each choice to the right function."""
    sessions = load_sessions()  # Start by loading saved sessions from the file.
    while True:  # Keep showing the menu until the user chooses 0.
        print("\n1) Add  2) Show all  3) Total hours  4) Summary  0) Exit")
        choice = input("Choose: ")
        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            for session in sessions:
                print(session)
        elif choice == "3":
            print("Total hours:", total_hours(sessions))
        elif choice == "4":
            show_summary(sessions)
        elif choice == "0":
            print("Bye!")
            break  # Exit the while loop, so the program ends.
        else:
            print("Invalid choice")  # Any other input.


# Run main() only when this file is run directly (not when imported).
if __name__ == "__main__":
    main()


