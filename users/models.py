from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    username = models.CharField(max_length=20)
    image = models.ImageField()
    email = models.EmailField(max_length=320)
    teams_count = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    time_created = models.DateTimeField()
    created_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, related_name='user_creator')
    time_updated = models.DateTimeField()
    updated_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, related_name='user_modifier')

    def __str__(self):
        return self.username

    def reached_team_limit(self):
        return self.teams_count <= 5