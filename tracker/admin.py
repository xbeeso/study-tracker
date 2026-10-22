from django.contrib import admin

from .models import Course, Session  # The dot means "from this same app folder".

# Registering a model tells Django: "build admin pages for this table".
# Django creates the add / edit / delete pages for us automatically.
admin.site.register(Course)
admin.site.register(Session)
