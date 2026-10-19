from datetime import date 

class StudySession:
    def __init__(self, course, minutes, note="", day=None):
        self.course = course
        self.minutes = minutes
        self.note = note
        self.day = day if day else date.today()    
        
    def __str__(self):
        return f"{self.day} | {self.course} | {self.minutes} min | {self.note}"

def total_hours(sessions):
    total_minutes = 0
    for session in sessions:
        total_minutes += session.minutes
    return round(total_minutes / 60, 1)

def hours_for_course(sessions, course_name):
    total_minutes = 0
    for session in sessions:
        if session.course == course_name:
            total_minutes += session.minutes
    return round(total_minutes / 60, 1)

def sessions_count(sessions, course_name):
    total_sessions = 0
    for session in sessions:
        if session.course == course_name:
            total_sessions += 1
    return total_sessions

sessions = [
    StudySession("Python 101", 90, "loops"),
    StudySession("SQL 101", 60, "SELECT"),
    StudySession("Python 101", 30, "functions"),
]

for session in sessions:
    print(session)
print("Total hours:", total_hours(sessions))
print("Python 101 hours:", hours_for_course(sessions, "Python 101"))
print("Python 101 sessions:", sessions_count(sessions, "Python 101"))

