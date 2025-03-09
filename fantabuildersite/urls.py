from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", include("users.urls")),
    path('account/', include('django.contrib.auth.urls')),
    path("teams/", include("teams.urls")),
]
