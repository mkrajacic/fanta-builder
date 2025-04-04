from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from teams.models import Singer

class Rules(models.Model):
    rule = models.TextField()

    def __str__(self):
        return self.rule
    
class Event(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Occurrence(models.Model):
    class OutcomeChoices(models.TextChoices):
        BONUS = 'BONUS', 'Bonus' 
        PENALTY = 'PENALTY', 'Penalty'

    occurrence = models.TextField()
    outcome = models.CharField(
        max_length=10,
        choices=OutcomeChoices.choices, 
        default=OutcomeChoices.BONUS
    )
    points = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)], default=1)

    def __str__(self):
        return self.occurrence

    def get_occurrences_by_outcome(self, outcome):
        return self.objects.filter(outcome=outcome)
    
class SingerOccurrence(models.Model):
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)
    occurrence = models.ForeignKey(Occurrence, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('singer', 'occurrence', 'event')

    def __str__(self):
        return str(self.occurrence) + str(self.singer) + str(self.event)
    