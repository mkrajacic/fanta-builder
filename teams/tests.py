import datetime
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
from unittest.mock import patch, MagicMock
import logging
logger = logging.getLogger('custom_logger')

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

    """def test_get_queryset_exception_handling(self):
        user = TestFunctions.add_user("mk")
        self.request.user = user
        self.client.force_login(user)

        with patch.object(user.team_set, 'all', side_effect=Exception('Test error')):
            response = self.client.get(reverse('teams:index')) 

            self.assertEqual(response.status_code, 200)
            self.assertQuerySetEqual(response.context['data'], Team.objects.none())

        with self.assertLogs('custom_logger', level="ERROR") as cm:
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