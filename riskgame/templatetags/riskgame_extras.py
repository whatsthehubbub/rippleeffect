from django import template

from riskgame.models import TeamJoinRequest, Events

import hashlib

register = template.Library()

@register.filter
def requested_join(player, team):
    try:
        TeamJoinRequest.objects.get(player=player, team=team)
        return True
    except TeamJoinRequest.DoesNotExist:
        return False

@register.filter
def event_name(event_code):
    return Events.reverse.get(event_code, '').replace('_', ' ').title()

@register.filter
def team_color(team):
    # returns the calculated color for the team (derived from the team name) as a hex value
    if team.name:
        m = hashlib.md5()
        m.update(team.name)

        return '#%s' % m.hexdigest()[:6]
    return "#CFC59F"

@register.filter
def player_color(player):
    # returns the calculated color for the player (derived from the player's email address) as a hex value
    m = hashlib.md5()
    m.update(player.email())

    return '#%s' % m.hexdigest()[:6]

@register.filter(name='times')
def times(number):
    return range(number)
