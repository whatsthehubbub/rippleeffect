from django import template

from riskgame.models import Player, Team, TeamJoinRequest

register = template.Library()

@register.filter
def requested_join(player, team):
    try:
        TeamJoinRequest.objects.get(player=player, team=team)
        return True
    except TeamJoinRequest.DoesNotExist:
        return False