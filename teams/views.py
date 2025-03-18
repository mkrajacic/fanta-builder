from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Team, Singer, TeamMember
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from django.contrib.auth import get_user_model
User=get_user_model()
from django.conf import settings
import json

class ShowTeams(LoginRequiredMixin, generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        return self.request.user.team_set.all()
    
    def get_context_data(self, **kwargs):
        ctx = super(ShowTeams, self).get_context_data(**kwargs)
        user_teams = self.request.user.team_set.all()
        teams_data = []
        for team in user_teams:
            team_member_singers = team.get_members_with_singers()
            team_singers_count = len(team_member_singers)
            teams_data.append({
                'team': team,
                'singers': team_member_singers,
                'singers_count': team_singers_count
            })
        
        ctx['data'] = teams_data
        ctx['data_count'] = len(teams_data)
        return ctx

@login_required
def edit_members(request, team_id):
    if request.method == "POST":
        json_string_choices = request.POST['choices']
        choices = json.loads(json_string_choices)
        captain = request.POST['captain']

        team = get_object_or_404(Team, pk=team_id)
        new_members = []
        current_members = TeamMember.objects.filter(team_id=team.id)

        for current_member in current_members:
            if current_member.id not in choices:
                member_to_delete = get_object_or_404(TeamMember, team_id=current_member.team, singer_id=current_member.singer)
                member_to_delete.delete()

        for choice in choices:
            if not TeamMember.team_contains_member(TeamMember, team_id, choice):
                new_members.append(TeamMember(team_id=team_id, singer_id=choice))
            if choice == captain:
                new_captain = get_object_or_404(Singer, pk=choice)
                team.captain = new_captain
                team.save()

        TeamMember.objects.bulk_create(new_members)
        return HttpResponse(status=204, headers={'HX-Trigger': 'memberListChanged'})
    else:
        user = request.user
        team = get_object_or_404(user.team_set, pk=team_id)
        singers = Singer.objects.all()
        max_points = settings.MAXIMUM_USABLE_POINTS
        max_slots = settings.MEMBERS_PER_TEAM
        form_action = reverse('teams:edit-members', kwargs={'team_id': team_id})
    
    return render(request, "edit-members.html", {
        "team": team,
        "singers": singers,
        "max_points": max_points,
        "max_slots": max_slots,
        "form_action": form_action,
    })

@login_required
def edit_members_success(request):
    return HttpResponse("it works")
    
class ViewTeam(generic.DetailView):
    model = Team
    template_name = "teams/view-team.html"

    def get_queryset(self):
        #return Team.objects.filter(data_pub__lte=timezone.now(), scelta__isnull=False).distinct()
        return "ecco"
