from django.contrib import admin
from .models import Team, TeamMember

class TeamMemberInline(admin.StackedInline):
    model = TeamMember
    extra = 5

class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", "team_image"]}),
    ]
    inlines = [TeamMemberInline]

admin.site.register(Team, TeamAdmin)
