from datetime import date

from django.db import models


class Course(models.Model):
    """A course you study, e.g. "Python 101". Each name is stored ONCE."""

    # CharField = short text. max_length is required for text fields.
    name = models.CharField(max_length=100)

    def __str__(self):
        # How a course appears in the admin panel and when printed.
        return self.name


class Session(models.Model):
    """One study session. It points to its course instead of repeating the name."""

    # ForeignKey = a link to a row in the Course table.
    # on_delete=CASCADE: if a course is deleted, its sessions are deleted too.
    # related_name="sessions": lets us go from a course to its sessions.
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sessions")
    # PositiveIntegerField: the database itself refuses negative numbers.
    minutes = models.PositiveIntegerField()
    # blank=True: the note is optional (can be left empty).
    note = models.CharField(max_length=200, blank=True)
    # default=date.today: today's date if we don't give one.
    # No brackets on purpose: Django calls it later, when each session is created.
    day = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.course} - {self.minutes} min"
    