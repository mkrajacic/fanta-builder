from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()

class Team(models.Model):
    name = models.CharField(max_length=50)
    team_image = models.ImageField()

    def __str__(self):
        return self.name

class Singer(models.Model):
    name = models.CharField(max_length=50)
    song = models.CharField(max_length=100)
    singer_image = models.ImageField()

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='team_member_assignor')

    def __str__(self):
        return self.team + ';' + self.singer
    