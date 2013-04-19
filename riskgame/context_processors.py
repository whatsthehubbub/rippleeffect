# -*- coding: utf-8
from riskgame.models import Player, TeamPlayer, EpisodeDay

def player(request):
    returnDict = {}
    
    if request.user.is_authenticated():
        try:
            currentPlayer = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            currentPlayer = Player.objects.create(user=request.user)

        returnDict['current_player'] = currentPlayer

        try:
            returnDict['current_teamplayer'] = TeamPlayer.objects.get(player=currentPlayer)
        except TeamPlayer.DoesNotExist:
            pass

        try:
            returnDict['current_day'] = EpisodeDay.objects.get(current=True)
        except EpisodeDay.DoesNotExist:
            pass

    # try:
    #     game = Game.objects.get_latest_game()
    #     returnDict['game'] = game
    # except:
    #     pass

    return returnDict
