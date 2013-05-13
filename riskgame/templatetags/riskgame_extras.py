from django import template

from riskgame.models import TeamJoinRequest, Events, TeamPlayer

import hashlib
import colorsys
import math


register = template.Library()

@register.filter
def requested_join(player, team):
    try:
        TeamJoinRequest.objects.get(player=player, team=team)
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
def team_color(team):
    # returns the calculated color for the team (derived from the team name) as a hex value
    if team and team.name:
        return colorify(team.name + str(team.id) + "", 0.1518, 0.8784)

    return "#CFC59F"

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

def colorify(str, s, v):
    m = hashlib.md5()
    m.update(str)

    # get a hue value by chopping the first two digits off a hex digest
    hue = int(m.hexdigest()[:4], 16) # yields an 8-bit integer; 0-255
    #print "raw hue", str, hue

    hue = hue / (255*255*1.0) # map 0-255 to 0-1 for colorsys
    #print "normalized hue", str, hue

    # compute rgb values based on our new h value, and preset s and v values
    rgb = colorsys.hsv_to_rgb(hue, s, v)

    # scale the rgb 0-1 range back to 0-255
    rgb = tuple([int(math.floor(255.0*x)) for x in rgb])

    # convert the rgb values to hex
    return '#%02x%02x%02x' % rgb
