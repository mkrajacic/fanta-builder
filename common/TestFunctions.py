from teams.models import Team, Singer, TeamMember
from django.contrib.auth import get_user_model
User=get_user_model()
import logging
logger = logging.getLogger('custom_logger')

def add_user(username):
    return User.objects.create(username=username)

def add_team(name, user, captain=None):
    return Team.objects.create(name=name, user_id=user, captain_id=captain)

def add_singer(name, song, cost=0):
    return Singer.objects.create(name=name, song=song, points_cost=cost)

def add_team_member(team_id, singer_id):
    return TeamMember.objects.create(team_id=team_id, singer_id=singer_id)

def add_filled_team(user_id, member_count=5):
    team = add_team("test team", user_id)
    for x in range(1, member_count):
        singer = add_singer(f"singer {x}", f"song {x}")
        add_team_member(team.id, singer.id)

    return team