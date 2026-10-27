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
        path("courses/", views.course_list, name="course_list"),
    # <int:pk> = a number in the address. Django passes it to the view as "pk".
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    # The session's number is in the address, like the course pages.
    path("sessions/<int:pk>/edit/", views.edit_session, name="edit_session"),
    path("sessions/<int:pk>/delete/", views.delete_session, name="delete_session"),
    
    
]


