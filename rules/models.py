from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Rules(models.Model):
    rule = models.TextField()

    def __str__(self):
        return self.rule

class Occurrence(models.Model):
    occurence = models.TextField()
    outcome = models.TextChoices("BONUS", "PENALTY")
    points = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)], default=1)

    def __str__(self):
        return self.occurence
    