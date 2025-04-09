from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Team, Singer, TeamMember
from results.models import TeamResult
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
from .forms import TeamForm
import logging
logger = logging.getLogger('custom_logger')

max_points = settings.MAXIMUM_USABLE_POINTS
max_slots = settings.MEMBERS_PER_TEAM
max_teams = settings.MAXIMUM_TEAMS_PER_USER
teams_readonly = settings.TEAMS_READONLY

class ShowTeams(LoginRequiredMixin, generic.ListView):
    template_name = "teams/index.html"

    def get_queryset(self):
        #logger.error("test")
        try:
            return self.request.user.team_set.all()
        except Exception as e:
            logger.error(f"Exception while fetching user team data: {e}")
            return self.request.user.team_set.none()
    
    def get_context_data(self, **kwargs):
        ctx = super(ShowTeams, self).get_context_data(**kwargs)

        try:
            user_teams = self.request.user.team_set.all()
            teams_data = []
            for team in user_teams:
                team_member_singers = team.get_members_with_singers()
                team_singers_count = len(team_member_singers)

                team_data = {}
                team_data['team'] = team
                team_data['singers'] = team_member_singers
                team_data['singers_count'] = team_singers_count

                if teams_readonly:
                    team_results_dict = {}
                    try:
                        team_results = get_object_or_404(TeamResult, team_id=team.id)
                        team_results_dict = {
                            "total_points": team_results.total_points,
                            "details": team_results.details
                        }
                    except Exception as e:
                        logger.error(f"Exception while fetching user team results: {e}")

                    team_data['team_results'] = team_results_dict

                teams_data.append(team_data)
            
            ctx['data'] = teams_data
            ctx['data_count'] = len(teams_data)
            ctx['max_teams'] = max_teams
            ctx['teams_readonly'] = teams_readonly
        except Exception as e:
            logger.error(f"Exception while fetching user team data with context: {e}")
            ctx['data'] = []
            ctx['data_count'] = 0
            ctx['max_teams'] = 0
            ctx['teams_readonly'] = teams_readonly

        return ctx
    
class ShowSingers(generic.ListView):
    template_name = "singers/index.html"
    context_object_name = "singers"

    def get_queryset(self):
        try:
            singers = Singer.objects.all()
            self.queryset = singers
            self.extra_context = {"singers_count": len(singers)}
            return super().get_queryset()
        except Exception as e:
            logger.error(f"Exception while fetching singer data: {e}")
            return Singer.objects.none()

@login_required
def edit_members(request, team_id):
    add_mode = request.GET.get("add")
    success_message = "Team members successfully updated"
    if add_mode == "true":
        add_mode = True
        success_message = "Team members successfully added"

    if request.method == "POST":

        if 'choices' not in request.POST:
            logger.error("There was an attempt to add team members without sending the member choices")
            return UtilityFunctions.toastTrigger(request, 400, "Failed to update team members! Please select members", "error")
        else:
            json_string_choices = request.POST['choices']

        try:
            choices = json.loads(json_string_choices)
            choices = [int(choice) for choice in choices]
        except Exception as e:
            logger.error(f"There was an attempt to add team members while passing an invalid choices value: {e}")
            return UtilityFunctions.toastTrigger(request, 400, "Failed to update team members! Please pass valid choices", "error")

        if 'captain' not in request.POST:
            logger.error("There was an attempt to add team members without picking a captain")
            return UtilityFunctions.toastTrigger(request, 400, "Failed to update team members! Please select a captain", "error")
        else:
            try:
                captain = int(request.POST['captain'])
            except ValueError:
                logger.error("There was an attempt to add team members while passing an invalid captain value")
                return UtilityFunctions.toastTrigger(request, 400, "Failed to update team members! Please select a valid captain", "error")

        if captain not in choices:
            logger.error("There was an attempt to add a team with a captain not among the selected choices")
            return UtilityFunctions.toastTrigger(request, 400, "Failed to update team members!", "error")

        if len(choices) != max_slots:
            logger.error("There was an attempt to add more or less team members than allowed")
            return UtilityFunctions.toastTrigger(request, 400, "Failed to update team members!", "error")

        team = get_object_or_404(Team, pk=team_id)

        sum_members = []
        new_members = []
        if not add_mode:
            try:
                current_members = TeamMember.objects.filter(team_id=team.id)
                for current_member in current_members:
                    if current_member.singer.id not in choices:
                        member_to_delete = get_object_or_404(TeamMember, team_id=current_member.team, singer_id=current_member.singer.id)
                        member_to_delete.delete()
                    else:
                        sum_members.append(current_member.singer.points_cost)
            except Exception as e:
                logger.error(f"Exception while fetching or deleting current team members: {e}")
                return UtilityFunctions.toastTrigger(request, 500, "Failed to update team members!", "error")

        for choice in choices:
            try:
                singer = get_object_or_404(Singer, pk=choice)
                if not TeamMember.team_contains_member(TeamMember, team_id, singer.id):
                    new_members.append(TeamMember(team_id=team_id, singer_id=singer.id))
                    sum_members.append(singer.points_cost)
                if singer.id == captain:
                    team.captain = singer
                    team.save()
            except Exception as e:
                logger.error(f"Exception while adding new team members: {e}")
                return UtilityFunctions.toastTrigger(request, 500, f"Failed to add team members!", "error")

        points_used = sum(sum_members)
        if points_used > max_points:
            logger.error("There was an attempt to add team members with a higher overall cost than allowed")
            return UtilityFunctions.toastTrigger(request, 400, "Failed to update team members!", "error")
            
        TeamMember.objects.bulk_create(new_members)
        return UtilityFunctions.toastTrigger(request, 204, success_message, "success", [{"teamDataChanged_" + str(team_id): None}])
        
    else:
        try:
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
        except Exception as e:
            logger.error(f"Exception while fetching team or singer data: {e}")
            return UtilityFunctions.toastTrigger(request, 204, f"Failed to retrive team or singer data", "error")
    
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
def add_team(request):
    success_message = "Team successfully added"
    form_action = reverse('teams:add-team')

    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data["name"]
            team_image = form.cleaned_data["team_image"]
            user = request.user

            try:
                if not user.reached_team_limit():
                    if team_image is not None:
                        team = Team.objects.create(name=name, user=user, team_image=team_image)
                    else:
                        team = Team.objects.create(name=name, user=user)
                else:
                    logger.error(f"User has tried to add a new team after surpassing their team limit")
                    return UtilityFunctions.toastTrigger(request, 400, f"Failed to add team, team limit has been reached!", "error")
            except Exception as e:
                logger.error(f"Exception while adding team: {e}")
                return UtilityFunctions.toastTrigger(request, 500, f"Failed to add team", "error")
            
            return UtilityFunctions.toastTrigger(request, 204, success_message, "success", [{"teamRefresh": None}])
        else:

            return render(request, "teams/edit-team.html", {
                "form": form,
                "form_action": form_action,
            })

    else:
        form = TeamForm()
    
        return render(request, "teams/edit-team.html", {
            "form": form,
            "form_action": form_action,
        })

@login_required
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    form_action = reverse('teams:edit-team', kwargs={'team_id': team_id})
    success_message = "Team information successfully updated"

    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES, instance=team)

        if form.is_valid():

            try:
                team = form.save(commit=False)
                team.user = request.user
                team.save()
            except Exception as e:
                logger.error(f"Exception while editing team: {e}")
                return UtilityFunctions.toastTrigger(request, 500, f"Failed to edit team", "error")
            
            return UtilityFunctions.toastTrigger(request, 204, success_message, "success", [{"teamDataChanged_" + str(team_id): None}])
        else:
        
            return render(request, "teams/edit-team.html", {
                "team": team,
                "form": form,
                "form_action": form_action,
            })

    else:
        form = TeamForm(instance=team)
    
    return render(request, "teams/edit-team.html", {
        "team": team,
        "form": form,
        "form_action": form_action,
    })

@login_required
def reload_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team_member_singers = team.get_members_with_singers()
    team_singers_count = len(team_member_singers)
    
    data = {}
    data['team'] = team
    data['singers'] = team_member_singers
    data['singers_count'] = team_singers_count
    data['max_points'] = max_points
    data['max_slots'] = max_slots
    
    is_htmx = request.headers.get('HX-Request') == 'true'
    if is_htmx:
        user_teams = request.user.team_set.all()
        data['data_count'] = len(user_teams)
        data['max_teams'] = max_teams,
        
    data['is_htmx'] = is_htmx

    return render(request, "teams/team.html", data)

@login_required
def reload_teams(request):
    user_teams = request.user.team_set.all()
    
    teams_data = []
    for team in user_teams:
        team_member_singers = team.get_members_with_singers()
        team_singers_count = len(team_member_singers)
        teams_data.append({
            'team': team,
            'singers': team_member_singers,
            'singers_count': team_singers_count
        })
    
    data = {}
    data['data'] = teams_data
        
    is_htmx = request.headers.get('HX-Request') == 'true'
    if is_htmx:
        data['max_teams'] = max_teams
        data['data_count'] = len(teams_data)
        
    data['is_htmx'] = is_htmx
    
    return render(request, "teams/show-teams.html", data)

@login_required
def delete_team(request, team_id):

    if not team_id:
        logger.error("There was an attempt to delete a team without passing a team id")
        return UtilityFunctions.toastTrigger(request, 400, "Failed to delete team", "error")

    success_message = "Team successfully deleted"

    if request.method == "DELETE":
        team = get_object_or_404(Team, pk=team_id)

        try:
            team.delete()
        except Exception as e:
            logger.error(f"Exception while deleting team: {e}")
            return UtilityFunctions.toastTrigger(request, 500, f"Failed to delete team", "error")
        
        return UtilityFunctions.toastTrigger(request, 204, success_message, "success", [{"teamRefresh": None}])

@login_required
def update_captain(request):
    success_message = "Team captain successfully changed"

    if request.method == "POST":

        if 'team_id' not in request.POST:
            logger.error("There was an attempt to update a captain without passing a team")
            return UtilityFunctions.toastTrigger(request, 400, "Failed to update team captain!", "error")
        else:
            team_id = request.POST['team_id']

        if 'captain_id' not in request.POST:
            logger.error("There was an attempt to update a captain without passing a captain")
            return UtilityFunctions.toastTrigger(request, 400, "Failed to update team captain!", "error")
        else:
            captain_id = request.POST['captain_id']

        try:
            team = get_object_or_404(Team, pk=team_id)
            singer = get_object_or_404(Singer, pk=captain_id)

            team.captain = singer
            team.save()
            return UtilityFunctions.toastTrigger(request, 204, success_message, "success", [{"teamDataChanged_" + str(team_id): None}])
        except Exception as e:
            logger.error(f"Exception while updating team captain: {e}")
            return UtilityFunctions.toastTrigger(request, 500, "Failed to update team captain!", "error")
