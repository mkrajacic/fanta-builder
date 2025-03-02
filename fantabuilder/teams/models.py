import datetime
from django.db import models
from django.utils import timezone
from users.models import User

class Team(models.Model):
    name = models.CharField(max_length=50)
    team_image = models.ImageField()
    time_created = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    time_updated = models.DateTimeField()
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
"""
    def era_pubblicato_recemente(self):
        adesso = timezone.now()
        return adesso - datetime.timedelta(days=1) <= self.data_pub <= adesso
"""

class Singer(models.Model):
    name = models.CharField(max_length=50)
    song = models.CharField(max_length=100)
    singer_image = models.ImageField()
    time_created = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    time_updated = models.DateTimeField()
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    scelta_testo = models.CharField(max_length=200)
    voti = models.IntegerField(default=0)

    def __str__(self):
        return self.scelta_testo
    