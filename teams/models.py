from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
User=get_user_model()
max_usable_points = settings.MAXIMUM_USABLE_POINTS

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    team_image = models.ImageField(upload_to="uploads", null=True)

    def __str__(self):
        return self.name

class Singer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    song = models.CharField(max_length=100)
    singer_image = models.ImageField(upload_to="uploads", null=True)
    points_cost = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(max_usable_points)], default=0)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='team_member_assignor')

    class Meta:
        unique_together = ('team', 'singer')

    def __str__(self):
        return self.team + ';' + self.singer
    