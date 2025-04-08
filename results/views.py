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
from django.db.models import Q
from django.core.paginator import Paginator

max_points = settings.MAXIMUM_USABLE_POINTS
max_slots = settings.MEMBERS_PER_TEAM
max_teams = settings.MAXIMUM_TEAMS_PER_USER

class ResultsSingers(generic.ListView):
    template_name = "results/singers.html"
    context_object_name = "singer_results"

    def get_queryset(self):
        singer_results = SingerResult.objects.annotate(
            rank=Window(
                expression=Rank(),  
                order_by=F('total_points').desc()
            )
        ).order_by('-total_points')
        self.queryset = singer_results
        self.extra_context = {"results_count": len(singer_results)}
        return super().get_queryset()
    
class ShowLeaderboards(generic.ListView):
    model = TeamResult
    template_name = "results/leaderboards.html"
    context_object_name = 'teams'
    paginate_by = 10

    def get_queryset(self):
        leaderboards_data = TeamResult.objects.annotate(
            display_rank=Window(
                expression=Rank(),
                order_by=F('total_points').desc()
            )
        ).select_related('team').order_by('-total_points')
        self.queryset = leaderboards_data
        self.extra_context = {"leaderboard_count": len(leaderboards_data)}
        return super().get_queryset()
    
@login_required
def search(request):
    search_query = request.GET.get('searchQuery', '')
    base_query = TeamResult.objects.select_related('team').order_by('-total_points')

    if search_query and len(search_query) >= 3:
        base_query = base_query.filter(
            Q(team__name__icontains=search_query) |
            Q(team__captain__name__icontains=search_query)
        )

    ranked_queryset = base_query.annotate(
        display_rank=Window(
            expression=Rank(),
            order_by=F('total_points').desc()
        )
    )

    paginator = Paginator(ranked_queryset, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "results/search-results.html", {
        'teams': page_obj,
        'search_term': search_query,
        'page_obj': page_obj,
    })
