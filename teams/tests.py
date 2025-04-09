import datetime
from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from common import TestFunctions
from django.test import RequestFactory
from django.urls import reverse
from teams import views
from .models import Team
from django.contrib.auth import get_user_model
User=get_user_model()
from django.contrib.auth.models import AnonymousUser
from django.test import Client
import logging
logger = logging.getLogger('custom_logger')
import json

class TeamListViewTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('teams:index'))
        self.view = views.ShowTeams()
        self.view.setup(self.request)

    def test_show_teams_authorized(self):
        user = TestFunctions.add_user("mk")
        self.request.user = user
        response = views.ShowTeams.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_show_teams_unauthorized(self):
        self.request.user = AnonymousUser()
        response = views.ShowTeams.as_view()(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertIn('unauthorized', response.headers.get('Location'))

    """def test_logging_detected(self):
        user = TestFunctions.add_user("mk")
        self.request.user = user

        with self.assertLogs(logger='custom_logger', level='ERROR') as cm:
            self.view.get_queryset()
            self.assertEqual(cm.output, ["ERROR:custom_logger:test"])"""

    """def test_get_queryset_exception_handling(self):
        user = TestFunctions.add_user("mk")
        self.request.user = user
        self.client.force_login(user)

        with self.assertLogs(logger='custom_logger', level="ERROR") as cm:
            with patch.object(user.team_set, 'all') as mock_method:
                mock_method.side_effect = Exception("forced exception")
                response = self.client.get(reverse('teams:index')) 
                self.assertEqual(cm.output, "d")"""

class SingerListViewTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('singers'))
        self.view = views.ShowSingers()
        self.view.setup(self.request)

    def test_show_singers_unauthorized(self):
        self.request.user = AnonymousUser()
        self.view.setup(self.request)
        response = views.ShowSingers.as_view()(self.request)
        self.assertEqual(response.status_code, 200)


class TeamMemberUpdateTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = TestFunctions.add_user("mk")
        self.c.force_login(self.user)
        self.team = TestFunctions.add_team("t1", self.user.id)

    def test_team_member_update_success(self):
        s1 = TestFunctions.add_singer("singer 1", f"song 1")
        s2 = TestFunctions.add_singer("singer 2", f"song 2")
        s3 = TestFunctions.add_singer("singer 3", f"song 3")
        s4 = TestFunctions.add_singer("singer 4", f"song 4")
        s5 = TestFunctions.add_singer("singer 5", f"song 5")

        choices = json.dumps([
            str(s1.id),
            str(s2.id),
            str(s3.id),
            str(s4.id),
            str(s5.id)
        ])
        post_data = {
            'choices': choices,
            'captain': s5.id
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 204)

    def test_team_member_update_not_enough_members(self):
        s1 = TestFunctions.add_singer("singer 1", f"song 1")
        s2 = TestFunctions.add_singer("singer 2", f"song 2")
        s3 = TestFunctions.add_singer("singer 3", f"song 3")
        s4 = TestFunctions.add_singer("singer 4", f"song 4")
        s5 = TestFunctions.add_singer("singer 5", f"song 5")

        choices = json.dumps([
            str(s1.id),
            str(s2.id),
            str(s3.id),
            str(s5.id)
        ])
    
        post_data = {
            'choices': choices,
            'captain': s2.id
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 400)

    def test_team_member_update_too_many_members(self):
        s1 = TestFunctions.add_singer("singer 1", f"song 1")
        s2 = TestFunctions.add_singer("singer 2", f"song 2")
        s3 = TestFunctions.add_singer("singer 3", f"song 3")
        s4 = TestFunctions.add_singer("singer 4", f"song 4")
        s5 = TestFunctions.add_singer("singer 5", f"song 5")
        s6 = TestFunctions.add_singer("singer 6", f"song 6")

        choices = json.dumps([
            str(s1.id),
            str(s2.id),
            str(s3.id),
            str(s4.id),
            str(s5.id),
            str(s6.id),
        ])
        post_data = {
            'choices': choices,
            'captain': s3.id
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 400)

    def test_team_member_update_unexisting_member(self):
        s1 = TestFunctions.add_singer("singer 1", f"song 1")
        s2 = TestFunctions.add_singer("singer 2", f"song 2")
        s3 = TestFunctions.add_singer("singer 3", f"song 3")
        s4 = TestFunctions.add_singer("singer 4", f"song 4")

        choices = json.dumps([
            str(s1.id),
            str(s2.id),
            str(s3.id),
            str(s4.id),
            str(666),
        ])
        
        post_data = {
            'choices': choices,
            'captain': s3.id
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 500)

    def test_team_member_update_invalid_member(self):

        s1 = TestFunctions.add_singer("singer 1", f"song 1")
        s2 = TestFunctions.add_singer("singer 2", f"song 2")
        s3 = TestFunctions.add_singer("singer 3", f"song 3")
        s4 = TestFunctions.add_singer("singer 4", f"song 4")

        choices = json.dumps([
            str(s1.id),
            str(s2.id),
            str(s3.id),
            str(s4.id),
            int(66),
        ])

        post_data = {
            'choices': choices,
            'captain': s3.id
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 500)

    def test_team_member_update_without_captain(self):
        s1 = TestFunctions.add_singer("singer 1", f"song 1")
        s2 = TestFunctions.add_singer("singer 2", f"song 2")
        s3 = TestFunctions.add_singer("singer 3", f"song 3")
        s4 = TestFunctions.add_singer("singer 4", f"song 4")
        s5 = TestFunctions.add_singer("singer 5", f"song 5")

        choices = json.dumps([
            str(s1.id),
            str(s2.id),
            str(s3.id),
            str(s4.id),
            str(s5.id),
        ])

        post_data = {
            'choices': choices
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 400)

    def test_team_member_update_with_invalid_captain(self):

        s1 = TestFunctions.add_singer("singer 1", f"song 1")
        s2 = TestFunctions.add_singer("singer 2", f"song 2")
        s3 = TestFunctions.add_singer("singer 3", f"song 3")
        s4 = TestFunctions.add_singer("singer 4", f"song 4")
        s5 = TestFunctions.add_singer("singer 5", f"song 5")
        s6 = TestFunctions.add_singer("singer 6", f"song 6")

        choices = json.dumps([
            str(s1.id),
            str(s2.id),
            str(s3.id),
            str(s4.id),
            str(s5.id),
            str(s6.id),
        ])

        post_data = {
            'choices': choices,
            'captain': "rose villain"
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 400)

    def test_team_member_update_with_captain_only(self):
        post_data = {
            'captain': 2
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 400)

    def test_team_member_update_with_invalid_members(self):
        post_data = {
            'choices': "invalid",
            'captain': 2
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 400)

    def test_team_member_update_with_captain_outside_team(self):
        s1 = TestFunctions.add_singer("singer 1", f"song 1")
        s2 = TestFunctions.add_singer("singer 2", f"song 2")
        s3 = TestFunctions.add_singer("singer 3", f"song 3")
        s4 = TestFunctions.add_singer("singer 4", f"song 4")
        s5 = TestFunctions.add_singer("singer 5", f"song 5")
        s6 = TestFunctions.add_singer("singer 6", f"song 6")

        choices = json.dumps([
            str(s1.id),
            str(s2.id),
            str(s3.id),
            str(s4.id),
            str(s5.id),
        ])
        post_data = {
            'choices': '["1","2","3","4","5"]',
            'captain': s6.id
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 400)

    def test_team_member_update_with_too_costly_members(self):
        max_points = settings.MAXIMUM_USABLE_POINTS
        costly_singer1 = TestFunctions.add_singer("c1", "c1", max_points)
        costly_singer2 = TestFunctions.add_singer("c2", "c2", max_points)
        costly_singer3 = TestFunctions.add_singer("c3", "c3", max_points)
        costly_singer4 = TestFunctions.add_singer("c4", "c4", max_points)
        costly_singer5 = TestFunctions.add_singer("c5", "c5", max_points)

        choices = json.dumps([
            str(costly_singer1.id),
            str(costly_singer2.id),
            str(costly_singer3.id),
            str(costly_singer4.id),
            str(costly_singer5.id)
        ])

        post_data = {
            'choices': choices,
            'captain': costly_singer3.id
        }
        response = self.c.post(reverse('teams:edit-members', kwargs={"team_id": self.team.pk}), post_data)
        self.assertEqual(response.status_code, 400)


class CaptainUpdateTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = TestFunctions.add_user("mk")
        self.c.force_login(self.user)
        self.singer = TestFunctions.add_singer("captain singer", "captain song")

    def test_captain_update_success(self):
        team = TestFunctions.add_filled_team(self.user.id)
        post_data = {
            'team_id': team.id,
            'captain_id': self.singer.id
        }
        response = self.c.post(reverse('teams:update-captain'), post_data)
        self.assertEqual(response.status_code, 204)

    def test_captain_update_missing_team(self):
        TestFunctions.add_filled_team(self.user.id)
        post_data = {
            'captain_id': self.singer.id
        }
        response = self.c.post(reverse('teams:update-captain'), post_data)
        self.assertEqual(response.status_code, 400)

    def test_captain_update_missing_captain(self):
        team = TestFunctions.add_filled_team(self.user.id)
        post_data = {
            'team_id': team.id
        }
        response = self.c.post(reverse('teams:update-captain'), post_data)
        self.assertEqual(response.status_code, 400)

    def test_captain_update_empty_data(self):
        TestFunctions.add_filled_team(self.user.id)
        post_data = {}
        response = self.c.post(reverse('teams:update-captain'), post_data)
        self.assertEqual(response.status_code, 400)

    def test_captain_update_unexisting_captain(self):
        team = TestFunctions.add_filled_team(self.user.id)
        post_data = {
            'team_id': team.id,
            'captain_id': 777
        }
        response = self.c.post(reverse('teams:update-captain'), post_data)
        self.assertEqual(response.status_code, 500)

    def test_captain_update_unexisting_team(self):
        TestFunctions.add_filled_team(self.user.id)
        post_data = {
            'team_id': 888,
            'captain_id': self.singer.id
        }
        response = self.c.post(reverse('teams:update-captain'), post_data)
        self.assertEqual(response.status_code, 500)

    def test_captain_update_invalid_captain(self):
        team = TestFunctions.add_filled_team(self.user.id)
        post_data = {
            'team_id': team.id,
            'captain_id': "xxx"
        }
        response = self.c.post(reverse('teams:update-captain'), post_data)
        self.assertEqual(response.status_code, 500)

    def test_captain_update_invalid_team(self):
        team = TestFunctions.add_filled_team(self.user.id)
        post_data = {
            'team_id': "team.id",
            'captain_id': self.singer.id
        }
        response = self.c.post(reverse('teams:update-captain'), post_data)
        self.assertEqual(response.status_code, 500)

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