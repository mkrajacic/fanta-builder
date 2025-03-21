from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Rules(models.Model):
    rule = models.TextField()

    def __str__(self):
        return self.rule

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