from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import TeamResult, SingerResult
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from django.contrib.auth import get_user_model
User=get_user_model()
from django.conf import settings
import json
from urllib.parse import urlencode
from common import UtilityFunctions
from django.db.models import F, Window
from django.db.models.functions import Rank
import logging
logger = logging.getLogger('custom_logger')

max_points = settings.MAXIMUM_USABLE_POINTS
max_slots = settings.MEMBERS_PER_TEAM
max_teams = settings.MAXIMUM_TEAMS_PER_USER

class ResultsSingers(generic.ListView):
    template_name = "results/singers.html"
    context_object_name = "singer_results"

    def get_queryset(self):
        #singer_results = SingerResult.objects.all()
        singer_results = SingerResult.objects.annotate(
            rank=Window(
                expression=Rank(),  
                order_by=F('total_points').desc()
            )
        ).order_by('-total_points')
        self.queryset = singer_results
        self.extra_context = {"results_count": len(singer_results)}
        return super().get_queryset()
