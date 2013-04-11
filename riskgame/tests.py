from riskgame.models import *
import nose.tools as nt

# from django.utils import timezone
# import datetime

import logging
logging.getLogger('south').setLevel(logging.CRITICAL)

class TestGameInitialize(object):
    @classmethod
    def setupAll(self):
        team = Team.objects.create()
        Team.objects.all().update(resources_collected=10)

        user1 = EmailUser.objects.create(email='nobody@example.com')
        user2 = EmailUser.objects.create(email='somebody@example.com')

        player1 = Player.objects.create(user=user1)
        player2 = Player.objects.create(user=user2)

        TeamPlayer.objects.create(team=team, player=player1)
        TeamPlayer.objects.create(team=team, player=player2)

        game = Game.objects.get_latest_game()
        game.initialize()

        # Start the first day
        from riskgame.tasks import change_days
        change_days()

    def test_inspect(self):
        inspect_result = TeamPlayer.objects.all()[0].inspect('gather')

        nt.assert_equal(len(inspect_result), 4)

    def test_initialize(self):
        team = Team.objects.all()[0]

        nt.assert_equal(team.goal_zero_markers, 1)

        nt.assert_equal(team.victory_points, 0)
        nt.assert_equal(team.victory_points_episode, 0)
        nt.assert_equal(team.resources_collected, 0)
        nt.assert_equal(team.resources_collected_episode, 0)

    @classmethod
    def teardownAll(self):
        Game.objects.all().delete()
        EmailUser.objects.all().delete()
        Player.objects.all().delete()
        TeamPlayer.objects.all().delete()

