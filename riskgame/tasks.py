from celery import task

from django.utils import timezone
from django.db.models import Q

import logging
logger = logging.getLogger('sake')

@task()
def change_days():
    from riskgame.models import Team

    # For all Teams without a check datetime update their day
    teams = Team.objects.filter(Q(check_next=None) | Q(check_next__lte=timezone.now()))

    for team in teams:
        team.update_current_day()

        logger.info("Updating current day for team %s", str(team))
