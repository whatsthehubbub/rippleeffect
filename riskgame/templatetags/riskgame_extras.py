from django import template

from riskgame.models import TeamJoinRequest, Events, TeamPlayer

import hashlib
import colorsys
import math


register = template.Library()

@register.filter
def requested_join(player, team):
    try:
        TeamJoinRequest.objects.get(player=player, team=team, invite=False)
        return True
    except TeamJoinRequest.DoesNotExist:
        return False

@register.filter
def team_member(player, team):
    try:
        TeamPlayer.objects.get(team=team, player=player)
        return True
    except TeamPlayer.DoesNotExist:
        return False

@register.filter
def event_name(event_code):
    return Events.reverse.get(event_code, '').replace('_', ' ').title()

@register.filter
def player_color(player):
    # returns the calculated color for the player (derived from the player's email address) as a hex value
    
    if player and player.email():
        return colorify(player.email() + str(player.user.id) + player.get_teamplayer().role, 0.3602, 0.6314)
    return "#CFC59F"

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter
def subtract(value, arg):
    return value - arg
