from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from teams import views

urlpatterns = [
    path("", TemplateView.as_view(template_name='home.html'), name='home'),
    path("singers/", views.ShowSingers.as_view(), name='singers'),
    path("admin/", admin.site.urls),
    path("register/", include("users.urls")),
    path('account/', include('django.contrib.auth.urls')),
    path("teams/", include("teams.urls")),
    path("rules/", include("rules.urls")),
    path("results/", include("results.urls")),
    path("unauthorized/", TemplateView.as_view(template_name='unauthorized.html'), name='unauthorized')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)