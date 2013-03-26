from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django.forms import ModelForm

from django.contrib.auth.decorators import login_required

from django.views.generic import DetailView
from django.views.decorators.http import require_POST

from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions

from riskgame.models import *

@login_required
def index(request):
    t = loader.get_template('riskgame/index.html')
    
    c = RequestContext(request, {
        'teams': Team.objects.all(),
        'create_team_form': CreateTeamform()
    })

    return HttpResponse(t.render(c))


def pre_launch(request):
    t = loader.get_template('riskgame/pre_launch.html')

    c = RequestContext(request, {
        'game': Game.objects.get_latest_game()
    })

    return HttpResponse(t.render(c))


class CreateTeamform(ModelForm):
    class Meta:
        model = Team
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.form_class = 'form'
        self.helper.form_action = reverse('team_create')
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('name', css_class='input-block-level', placeholder='Name'),
            FormActions(
                Submit('submit', _('Send'), css_class='btn')
            )
        )

        super(CreateTeamform, self).__init__(*args, **kwargs)

@login_required
def team_create(request):
    if request.method == "POST":
        name = request.POST.get('name', '')

        player = request.user.get_or_create_player()
        Team.objects.create(name=name, leader=player)

        return HttpResponseRedirect(reverse('index'))


class TeamDetail(DetailView):
    model = Team
    template_name = 'riskgame/team_detail.html'
    context_object_name = 'team'

@login_required
@require_POST
def request_team_join(request, pk):
    player = request.user.get_or_create_player()
    team = Team.objects.get(id=pk)

    TeamJoinRequest.objects.create(team=team, player=player)

    return HttpResponseRedirect(reverse('team_detail', args=[player.team.id]))

@login_required
@require_POST
def accept_team_join(request, pk):
    join_request = TeamJoinRequest.objects.get(id=request.POST.get('join_request_id', ''))

    print join_request

    print request.user.get_or_create_player()
    print join_request.team.leader

    if request.user.get_or_create_player() == join_request.team.leader:
        player = join_request.player
        player.team = join_request.team
        player.save()

        join_request.delete()

        return HttpResponseRedirect(reverse('team_detail', args=[player.team.id]))


@login_required
def players(request):
    t = loader.get_template('riskgame/players.html')
    
    c = RequestContext(request, {
        'players': Player.objects.all()
    })

    return HttpResponse(t.render(c))
