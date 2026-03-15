from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    ClubCreateView,
    ClubDetailView,
    ClubListView,
    EventDeleteView,
    EventCreateView,
    EventUpdateView,
    HomeView,
    MyRegistrationsView,
    SignUpView,
    add_comment,
    cancel_registration,
    join_club,
    register_event,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("clubs/", ClubListView.as_view(), name="club_list"),
    path("clubs/new/", ClubCreateView.as_view(), name="club_create"),
    path("clubs/<int:pk>/", ClubDetailView.as_view(), name="club_detail"),
    path("clubs/<int:pk>/join/", join_club, name="join_club"),
    path("clubs/<int:club_pk>/events/new/", EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/edit/", EventUpdateView.as_view(), name="event_update"),
    path("events/<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
    path("events/<int:pk>/register/", register_event, name="register_event"),
    path("events/<int:pk>/comments/", add_comment, name="add_comment"),
    path("my-registrations/", MyRegistrationsView.as_view(), name="my_registrations"),
    path("registrations/<int:pk>/cancel/", cancel_registration, name="cancel_registration"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("register/", SignUpView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
