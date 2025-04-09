from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

max_teams_count = settings.MAXIMUM_TEAMS_PER_USER
class User(AbstractUser):
    pass
    first_name = None
    last_name = None
    image = models.ImageField(null=True, blank=True, default="unknown.svg")

    def __str__(self):
        return self.username
    
    def reached_team_limit(self):
        team_limit = settings.MAXIMUM_TEAMS_PER_USER
        teams_by_user_count = self.team_set.all().count()
        return teams_by_user_count >= team_limit