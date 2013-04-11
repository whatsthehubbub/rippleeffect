from riskgame.models import *
import nose.tools as nt

# from django.utils import timezone
# import datetime

class TestGame(object):
    def setup(self):
        game = Game.objects.get_latest_game()
        game.initialize()

        team = Team.objects.create()

        user1 = EmailUser.objects.create(email='nobody@example.com')
        user2 = EmailUser.objects.create(email='somebody@example.com')

        player1 = Player.objects.create(user=user1)
        player2 = Player.objects.create(user=user2)

        teamplayer1 = TeamPlayer.objects.create(team=team, player=player1)
        teamplayer2 = TeamPlayer.objects.create(team=team, player=player2)

        # Start the first day
        from riskgame.tasks import change_days
        change_days()

    def test_inspect(self):
        inspect_result = TeamPlayer.objects.all()[0].inspect('gather')

        print inspect_result
        nt.assert_equal(len(inspect_result), 4)

    def teardown(self):
        pass