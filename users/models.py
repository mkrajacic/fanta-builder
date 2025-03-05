from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

max_teams_count = settings.MAXIMUM_TEAMS_PER_USER
class User(AbstractUser):
    pass
    first_name = None
    last_name = None
    teams_count = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(max_teams_count)], default=0)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.username

    def reached_team_limit(self):
        return self.teams_count >= max_teams_count