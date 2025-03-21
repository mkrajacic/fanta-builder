from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "teams"
urlpatterns = [
    path("", views.ShowTeams.as_view(), name="index"),
    path("<int:team_id>/edit-members/", views.edit_members, name="edit-members"),
    path("edit-members-success/", views.edit_members_success, name="edit-members-success"),
    path("<int:pk>/", views.ViewTeam.as_view(), name="view-team"),
    #path("<int:pk>/modify", views.ModifyTeam.as_view(), name="modify-team"),
    #path("<int:pk>/modify-lineup", views.ModifyTeamLineup.as_view(), name="modify-team-lineup"),
]
