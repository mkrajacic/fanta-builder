from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "results"
urlpatterns = [
    path("singers", views.ResultsSingers.as_view(), name="results-singers"),
]
