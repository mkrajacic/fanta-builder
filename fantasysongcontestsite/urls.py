from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from teams import views as teamViews
from users import views as userViews

urlpatterns = [
    path("", TemplateView.as_view(template_name='home.html'), name='home'),
    path("singers/", teamViews.ShowSingers.as_view(), name='singers'),
    path("admin/", admin.site.urls),
    path("register/", include("users.urls")),
    path('account/', include('django.contrib.auth.urls')),
    path("teams/", include("teams.urls")),
    path("rules/", include("rules.urls")),
    path("results/", include("results.urls")),
    path("profile/", userViews.ProfileView, name="profile"),
    path("profile/<int:user_id>/edit/", userViews.edit_profile, name="edit-profile"),
    path("profile/<int:user_id>/reload-profile/", userViews.reload_profile, name="reload-profile"),
    path("unauthorized/", TemplateView.as_view(template_name='unauthorized.html'), name='unauthorized')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)