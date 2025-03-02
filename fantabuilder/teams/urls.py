from django.urls import path
from . import views

app_name = "teams"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.ViewTeam.as_view(), name="view-team"),
    #path("<int:pk>/modify", views.ModifyTeam.as_view(), name="modify-team"),
    #path("<int:pk>/modify-lineup", views.ModifyTeamLineup.as_view(), name="modify-team-lineup"),
]
