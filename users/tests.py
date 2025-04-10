from django.test import TestCase
from common import TestFunctions

class UserModelTests(TestCase):
    def test_surpassed_team_limit(self):
        user = TestFunctions.add_user("mk")
        for x in range(1,7):
            TestFunctions.add_team(f"team {x} name", user.id)

        self.assertTrue(user.reached_team_limit())

    def test_below_team_limit(self):
        user = TestFunctions.add_user("mk")
        for x in range(1,4):
            TestFunctions.add_team(f"team {x} name", user.id)

        self.assertFalse(user.reached_team_limit())
