from django.urls import path
from . import views

app_name = "results"
urlpatterns = [
    path("singers", views.ResultsSingers.as_view(), name="results-singers"),
    path("leaderboards", views.ShowLeaderboards.as_view(), name="leaderboards"),
    path("search", views.search, name="search"),
]
