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
from urllib.parse import urlencode
from django.contrib import messages
from common import UtilityFunctions

max_points = settings.MAXIMUM_USABLE_POINTS
max_slots = settings.MEMBERS_PER_TEAM

class ShowTeams(LoginRequiredMixin, generic.ListView):
    template_name = "teams/index.html"

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
    
class ShowSingers(generic.ListView):
    template_name = "singers/index.html"
    context_object_name = "singers"

    def get_queryset(self):
        singers = Singer.objects.all()
        self.queryset = singers
        self.extra_context = {"singers_count": len(singers)}
        return super().get_queryset()

@login_required
def edit_members(request, team_id):
    add_mode = request.GET.get("add")
    success_message = "Team members successfully updated"
    if add_mode == "true":
        add_mode = True
        success_message = "Team members successfully added"

    if request.method == "POST":
        json_string_choices = request.POST['choices']
        choices = json.loads(json_string_choices)
        captain = int(request.POST['captain'])

        team = get_object_or_404(Team, pk=team_id)
        new_members = []
        if not add_mode:
            current_members = TeamMember.objects.filter(team_id=team.id)
            for current_member in current_members:
                if current_member.id not in choices:
                    member_to_delete = get_object_or_404(TeamMember, team_id=current_member.team, singer_id=current_member.singer)
                    member_to_delete.delete()

        for choice in choices:
            singer = get_object_or_404(Singer, pk=choice)
            if not TeamMember.team_contains_member(TeamMember, team_id, singer.id):
                new_members.append(TeamMember(team_id=team_id, singer_id=singer.id))
            if singer.id == captain:
                team.captain = singer
                team.save()

        TeamMember.objects.bulk_create(new_members)
        return UtilityFunctions.toastTrigger(request, 204, success_message, "success", [{"teamDataChanged_" + str(team_id): None}])
    else:
        team = get_object_or_404(Team, pk=team_id)
        singers = Singer.objects.all()
        current_members_ids = []
        if add_mode:
            form_action = reverse('teams:edit-members', kwargs={'team_id': team_id})
            form_action += '?' + urlencode({"add": "true"})
        else:
            form_action = reverse('teams:edit-members', kwargs={'team_id': team_id})
            current_members = TeamMember.objects.filter(team_id=team.id)
            for current_member in current_members:
                current_members_ids.append(current_member.singer_id)
    
    return render(request, "teams/edit-members.html", {
        "team": team,
        "singers": singers,
        "max_points": max_points,
        "max_slots": max_slots,
        "form_action": form_action,
        "current_members": current_members_ids,
        "add_mode": "true" if add_mode == True else "false"
    })

@login_required
def edit_team(request, team_id):
    add_mode = request.GET.get("add")
    if add_mode == "true":
        add_mode = True

    if request.method == "POST":
        name = str(request.POST['name'])
        team_image = str(request.POST['team_image'])
        team = get_object_or_404(Team, pk=team_id)

        return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    "teamDataChanged": None,
                    "showMessage": "Teams information successfully updated"
                })})
    else:
        team = get_object_or_404(Team, pk=team_id)
        if add_mode:
            form_action = reverse('teams:edit-team', kwargs={'team_id': team_id})
            form_action += '?' + urlencode({"add": "true"})
        else:
            form_action = reverse('teams:edit-team', kwargs={'team_id': team_id})
    
    return render(request, "teams/edit-team.html", {
        "team": team,
        "form_action": form_action,
    })

@login_required
def reload_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team_member_singers = team.get_members_with_singers()
    team_singers_count = len(team_member_singers)

    return render(request, "teams/team.html", {
        'team': team,
        'singers': team_member_singers,
        'singers_count': team_singers_count,
        "max_points": max_points,
        "max_slots": max_slots,
    })

@login_required
def update_captain(request):
    success_message = "Team captain successfully changed"

    if request.method == "POST":
        team_id = request.POST['team_id']
        captain_id = request.POST['captain_id']
        team = get_object_or_404(Team, pk=team_id)
        singer = get_object_or_404(Singer, pk=captain_id)

        team.captain = singer
        team.save()
        return UtilityFunctions.toastTrigger(request, 204, success_message, "success", [{"teamDataChanged_" + str(team_id): None}])
