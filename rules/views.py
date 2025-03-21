from django.shortcuts import render, get_object_or_404
from .models import Rules, Occurrence
from django.views import generic
from django.utils import timezone
from django.contrib.auth import get_user_model
User=get_user_model()
from django.conf import settings

class ShowRules(generic.ListView):
    template_name = "rules/index.html"

    def get_queryset(self):
        return Rules.objects.all()
    
    def get_context_data(self, **kwargs):
        ctx = super(ShowRules, self).get_context_data(**kwargs)
        rules = Rules.objects.all()
        occurences = Occurrence.objects.all()
        bonuses = Occurrence.get_occurrences_by_outcome(Occurrence, "BONUS")
        penalties = Occurrence.get_occurrences_by_outcome(Occurrence, "PENALTY")
        
        ctx['rules'] = rules
        ctx['rules_count'] = len(rules)
        ctx['occurences_count'] = len(occurences)
        ctx['bonuses'] = bonuses
        ctx['penalties'] = penalties
        return ctx
