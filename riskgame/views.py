from django.http import HttpResponse
from django.template import RequestContext, loader
# from django.core.urlresolvers import reverse

from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from riskgame.models import *

@login_required
def index(request):
    t = loader.get_template('riskgame/index.html')
    
    c = RequestContext(request, {
        'teams': Team.objects.all()
    })

    return HttpResponse(t.render(c))


def pre_launch(request):
    t = loader.get_template('riskgame/pre_launch.html')

    c = RequestContext(request, {
        'game': Game.objects.get_latest_game()
    })

    return HttpResponse(t.render(c))


class TeamDetail(DetailView):
    model = Team
    template_name = 'riskgame/team_detail.html'
    context_object_name = 'team'
