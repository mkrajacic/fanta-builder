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
        
    def test_surpassed_points_limit(self):
        user = TestFunctions.add_user("mk")
        team = TestFunctions.add_team("test team", user.id)
        
        singer1 = TestFunctions.add_singer("singer 1", "song 1", 20)
        TestFunctions.add_team_member(team.id, singer1.id)
        singer2 = TestFunctions.add_singer("singer 2", "song 2", 20)
        TestFunctions.add_team_member(team.id, singer2.id)
        singer3 = TestFunctions.add_singer("singer 3", "song 3", 20)
        TestFunctions.add_team_member(team.id, singer3.id)
        singer4 = TestFunctions.add_singer("singer 4", "song 4", 20)
        TestFunctions.add_team_member(team.id, singer4.id)
        singer5 = TestFunctions.add_singer("singer 5", "song 5", 20)
        TestFunctions.add_team_member(team.id, singer5.id)

        self.assertTrue(team.reached_points_limit())

    def test_below_points_limit(self):
        user = TestFunctions.add_user("mk")
        team = TestFunctions.add_team("test team", user.id)
        
        singer1 = TestFunctions.add_singer("singer 1", "song 1", 2)
        TestFunctions.add_team_member(team.id, singer1.id)
        singer2 = TestFunctions.add_singer("singer 2", "song 2", 20)
        TestFunctions.add_team_member(team.id, singer2.id)
        singer3 = TestFunctions.add_singer("singer 3", "song 3", 10)
        TestFunctions.add_team_member(team.id, singer3.id)
        singer4 = TestFunctions.add_singer("singer 4", "song 4", 4)
        TestFunctions.add_team_member(team.id, singer4.id)
        singer5 = TestFunctions.add_singer("singer 5", "song 5", 6)
        TestFunctions.add_team_member(team.id, singer5.id)

        self.assertFalse(team.reached_points_limit())