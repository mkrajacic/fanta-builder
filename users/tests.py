import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from teams.models import Team, Singer, TeamMember
from django.contrib.auth import get_user_model
User=get_user_model()
from django.conf import settings

class UserModelTests(TestCase):
    def test_surpassed_team_limit(self):
        user = add_user("mk")
        for x in range(1,7):
            add_team(f"team {x} name", user.id)

        self.assertTrue(user.reached_team_limit())

    def test_below_team_limit(self):
        user = add_user("mk")
        for x in range(1,4):
            add_team(f"team {x} name", user.id)

        self.assertFalse(user.reached_team_limit())
        

def add_user(username):
    return User.objects.create(username=username)

def add_team(name, user):
    return Team.objects.create(name=name, user_id=user)

def add_singer(name, song):
    return Singer.objects.create(name=name, song=song)

def add_team_member(team_id, singer_id):
    return TeamMember.objects.create(team_id=team_id, singer_id=singer_id)