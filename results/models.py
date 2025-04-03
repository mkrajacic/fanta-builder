from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
User=get_user_model()
from teams.models import Team

class TeamResult(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, unique=True)
    total_points = models.IntegerField(default=0)
    details = models.JSONField(default=dict)
    