from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from teams.models import TeamMember, Team

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

    occurence = models.TextField()
    outcome = models.CharField(
        max_length=10,
        choices=OutcomeChoices.choices, 
        default=OutcomeChoices.BONUS
    )
    points = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)], default=1)

    def __str__(self):
        return self.occurence

    def get_occurrences_by_outcome(self, outcome):
        return self.objects.filter(outcome=outcome)

class MemberOccurrence(models.Model):
    occurrence = models.ForeignKey(Occurrence, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('occurrence', 'event', 'team_member')

    def __str__(self):
        return "Occurrence: " + str(self.occurrence) + " for event: " + str(self.event) + " for team member: " + str(self.team_member)
    