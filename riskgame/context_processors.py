# -*- coding: utf-8
from riskgame.models import Player

def player(request):
    returnDict = {}
    
    if request.user.is_authenticated():
        try:
            currentPlayer = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            currentPlayer = Player.objects.create(user=request.user)

        returnDict['player'] = currentPlayer

    # try:
    #     game = Game.objects.get_latest_game()
    #     returnDict['game'] = game
    # except:
    #     pass

    return returnDict
