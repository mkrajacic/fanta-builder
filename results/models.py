from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
User=get_user_model()
from teams.models import Team, Singer, TeamMember
from rules.models import Occurrence

class ScoreOccurance(models.Model):
    occurence = models.ForeignKey(Occurrence, on_delete=models.CASCADE)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('occurence', 'singer', 'team')

    def __str__(self):
        return self.occurence + ';' + self.singer + ';' + self.team
    
class ScoreOccuranceBonus(models.Model):
    occurence_score = models.ForeignKey(ScoreOccurance, on_delete=models.CASCADE)
    bonus_points = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)], default=1)
    bonus_basis = models.CharField(max_length=50)

    def __str__(self):
        return self.occurence_score + ';' + self.bonus_points
    