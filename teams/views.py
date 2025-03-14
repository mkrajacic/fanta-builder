from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Team
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.utils import timezone
from django.contrib.auth import get_user_model
User=get_user_model()

class ShowTeams(LoginRequiredMixin, generic.ListView):
    template_name = "index.html"
    context_object_name = "user_teams"

    def get_queryset(self):
        return self.request.user.team_set.all()
    
class ViewTeam(generic.DetailView):
    model = Team
    template_name = "teams/view-team.html"

    def get_queryset(self):
        #return Team.objects.filter(data_pub__lte=timezone.now(), scelta__isnull=False).distinct()
        return "ecco"
