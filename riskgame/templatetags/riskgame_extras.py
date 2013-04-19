from django import template

from riskgame.models import TeamJoinRequest, Events

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
    return Events.reverse.get(event_code, '').replace('_', ' ').lower()