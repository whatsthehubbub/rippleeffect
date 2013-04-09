from celery import task

from django.utils import timezone

from riskgame.models import Game, EpisodeDay

import logging
logger = logging.getLogger('riskgame')

@task()
def change_days():
    game = Game.objects.get_latest_game()

    if game.active():
        if not EpisodeDay.objects.filter(current=True).exists():
            first_day = EpisodeDay.objects.all().order_by('end')[0]
            first_day.current = True
            first_day.save()

            first_day.start()

            return first_day
        else:
            current_day = EpisodeDay.objects.get(current=True)

            if timezone.now() > current_day.end:
                current_day.current = False
                current_day.save()

                next_day = current_day.next
                next_day.current = True
                next_day.save()

                next_day.start()

                return next_day

@task()
def test_task():
    from datetime import datetime
    cyan = lambda text: "\033[1;36m%s\033[0m" % text
    print(cyan('[test_task:%s] processing task' % str(datetime.now())))
    