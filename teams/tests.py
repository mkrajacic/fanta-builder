import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Team, Singer, TeamMember
from django.contrib.auth import get_user_model
User=get_user_model()
from django.conf import settings

class TeamModelTests(TestCase):
    def test_surpassed_member_limit(self):
        user = add_user("mk")
        team = add_team("test team", user.id)
        for x in range(1,7):
            singer = add_singer(f"singer {x}", f"song {x}")
            add_team_member(team.id, singer.id)

        self.assertTrue(team.reached_member_limit())

    def test_below_member_limit(self):
        user = add_user("mk")
        team = add_team("test team", user.id)
        for x in range(1,4):
            singer = add_singer(f"singer {x}", f"song {x}")
            add_team_member(team.id, singer.id)

        self.assertFalse(team.reached_member_limit())
        

def add_user(username):
    return User.objects.create(username=username)

def add_team(name, user):
    return Team.objects.create(name=name, user_id=user)

def add_singer(name, song):
    return Singer.objects.create(name=name, song=song)

def add_team_member(team_id, singer_id):
    return TeamMember.objects.create(team_id=team_id, singer_id=singer_id)