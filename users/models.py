from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    first_name = None
    last_name = None
    teams_count = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.username

    def reached_team_limit(self):
        return self.teams_count <= 5