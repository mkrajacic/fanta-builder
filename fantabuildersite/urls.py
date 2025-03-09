from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name='home.html'), name='home'),
    path("admin/", admin.site.urls),
    path("register/", include("users.urls")),
    path('account/', include('django.contrib.auth.urls')),
    path("teams/", include("teams.urls")),
]
