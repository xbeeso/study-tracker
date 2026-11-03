from django.contrib import admin
from django.urls import include, path

# The main entrance: every request arrives here first.
urlpatterns = [
    path("admin/", admin.site.urls),  # Django's ready-made admin panel (day 5).
    # Django's ready-made login/logout pages: gives us /accounts/login/ and /accounts/logout/.
    path("accounts/", include("django.contrib.auth.urls")),
    # Everything else: send it to our app's address book.
    path("", include("tracker.urls")),
]
