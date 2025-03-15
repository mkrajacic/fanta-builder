from django.contrib import admin
from .models import Team, TeamMember, Singer

class TeamMemberInline(admin.StackedInline):
    model = TeamMember
    extra = 5

class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", "team_image", "user", "captain"]}),
    ]
    inlines = [TeamMemberInline]

admin.site.register(Team, TeamAdmin)
admin.site.register(Singer)