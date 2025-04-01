from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "teams"
urlpatterns = [
    path("", views.ShowTeams.as_view(), name="index"),
    path("<int:team_id>/edit-members/", views.edit_members, name="edit-members"),
    path("<int:team_id>/edit-team/", views.edit_team, name="edit-team"),
    path("add-team/", views.add_team, name="add-team"),
    path("update-captain/", views.update_captain, name="update-captain"),
    path("<int:team_id>/reload-team/", views.reload_team, name="reload-team"),
    path("reload-teams/", views.reload_teams, name="reload-teams"),
]
