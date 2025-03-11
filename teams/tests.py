import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from common import TestFunctions

class TeamModelTests(TestCase):
    def test_surpassed_member_limit(self):
        user = TestFunctions.add_user("mk")
        team = TestFunctions.add_team("test team", user.id)
        for x in range(1,7):
            singer = TestFunctions.add_singer(f"singer {x}", f"song {x}")
            TestFunctions.add_team_member(team.id, singer.id)

        self.assertTrue(team.reached_member_limit())

    def test_below_member_limit(self):
        user = TestFunctions.add_user("mk")
        team = TestFunctions.add_team("test team", user.id)
        for x in range(1,4):
            singer = TestFunctions.add_singer(f"singer {x}", f"song {x}")
            TestFunctions.add_team_member(team.id, singer.id)

        self.assertFalse(team.reached_member_limit())