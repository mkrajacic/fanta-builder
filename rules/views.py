from .models import Rules, Occurrence
from django.views import generic
from django.contrib.auth import get_user_model
User=get_user_model()

class ShowRules(generic.ListView):
    template_name = "rules/index.html"

    def get_queryset(self):
        return Rules.objects.all()
    
    def get_context_data(self, **kwargs):
        ctx = super(ShowRules, self).get_context_data(**kwargs)
        rules = Rules.objects.all()
        occurrences = Occurrence.objects.all()
        bonuses = Occurrence.get_occurrences_by_outcome(Occurrence, "BONUS")
        penalties = Occurrence.get_occurrences_by_outcome(Occurrence, "PENALTY")
        
        ctx['rules'] = rules
        ctx['rules_count'] = len(rules)
        ctx['occurrences_count'] = len(occurrences)
        ctx['bonuses'] = bonuses
        ctx['penalties'] = penalties
        return ctx
