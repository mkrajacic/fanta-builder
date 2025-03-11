from teams.models import Team, Singer, TeamMember
from django.contrib.auth import get_user_model
User=get_user_model()

def add_user(username):
    return User.objects.create(username=username)

def add_team(name, user):
    return Team.objects.create(name=name, user_id=user)

def add_singer(name, song):
    return Singer.objects.create(name=name, song=song)

def add_team_member(team_id, singer_id):
    return TeamMember.objects.create(team_id=team_id, singer_id=singer_id)