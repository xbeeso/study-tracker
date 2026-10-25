from django.urls import path

from . import views  # The dot means "from this same app folder".

# The app's address book: which address runs which view function.
urlpatterns = [
    # "" = the main page (nothing after the site address).
    path("", views.home, name="home"),
    # "about/" = the about page.
    path("about/", views.about, name="about"),
        # "add/" = the page with the add-session form.
    path("add/", views.add_session, name="add_session"),
]


