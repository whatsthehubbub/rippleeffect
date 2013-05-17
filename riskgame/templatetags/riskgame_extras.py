from django import template

from riskgame.models import TeamJoinRequest, Events, TeamPlayer, Team


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
def team_for_pk(pk):
    try:
        return Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return None

@register.filter
def event_name(event_code):
    return Events.reverse.get(event_code, '').replace('_', ' ').title()


@register.filter(name='times')
def times(number):
    return range(number)

@register.filter
def subtract(value, arg):
    return value - arg
