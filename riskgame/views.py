from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django.forms import ModelForm

from django.db.models import F

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import DetailView
from django.views.decorators.http import require_POST

from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions

from riskgame.models import *

import random

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

@login_required
def play(request):
    t = loader.get_template('riskgame/play.html')

    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)

    c = RequestContext(request, {
        'teamplayer': teamplayer,
        'teammates': teamplayer.team.teamplayer_set.all()
    })

    return HttpResponse(t.render(c))

@login_required
def play_prep(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    playerCount = team.players.count()

    gatherCards = (3*playerCount) * [0] + (3*playerCount) * [1]
    riskCards = (4*playerCount) * [0] + (2*playerCount) * [1]

    # Shuffle both piles
    random.shuffle(gatherCards)
    random.shuffle(riskCards)

    for tp in team.teamplayer_set.all():
        tp.startPiles()

        tp.gather_markers = 0
        tp.prevent_markers = 0

        # Add 6 gather cards
        # Add 6 risk cards
        for counter in range(6):
            tp.addGatherCard(gatherCards.pop())
            tp.addRiskCard(riskCards.pop())

        tp.save()

    Team.objects.filter(id=team.id).update(action_points=0)

    return HttpResponseRedirect(reverse('play'))

@login_required
def play_start_day(request):
    """Do the actions at the start of the day.

    For now: adding new action points, and incrementing the goal zero
    marker."""
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    playerCount = team.players.count()

    Team.objects.filter(id=team.id).update(action_points=4*playerCount)
    Team.objects.filter(id=team.id).update(goal_zero_markers=F('goal_zero_markers')+1)

    return HttpResponseRedirect(reverse('play'))

@login_required
def play_inspect(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    if team.action_points:
        Team.objects.filter(id=team.id).update(action_points=F('action_points')-1)

        pile = request.POST.get('pile', '')

        if pile:
            result = teamplayer.inspect(pile)
            teamplayer.save()

            messages.add_message(request, messages.INFO, "Inspected %s and found: %s" % (pile, ' '.join(result)))

    return HttpResponseRedirect(reverse('play'))


@login_required
def play_invest(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    if team.action_points:
        Team.objects.filter(id=team.id).update(action_points=F('action_points')-1)

        pile = request.POST.get('pile', '')

        if pile:
            teamplayer.invest(pile)
            teamplayer.save()

            # Add message
            messages.add_message(request, messages.INFO, "Invested in pile %s" % pile)

    return HttpResponseRedirect(reverse('play'))


@login_required
def play_gather(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    if team.action_points:
        Team.objects.filter(id=team.id).update(action_points=F('action_points')-1)

        teamplayer.gather()
        teamplayer.save()

        messages.add_message(request, messages.INFO, "Placed gather token.")

    return HttpResponseRedirect(reverse('play'))

@login_required
def play_prevent(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    if team.action_points:
        Team.objects.filter(id=team.id).update(action_points=F('action_points')-1)

        teamplayer.prevent()
        teamplayer.save()

        messages.add_message(request, messages.INFO, "Placed prevent token.")

    return HttpResponseRedirect(reverse('play'))

@login_required
def play_pump(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    oil, risks, preventions = teamplayer.pump()
    teamplayer.save()

    if risks > preventions:
        # We have an incident
        Team.objects.filter(id=team.id).update(goal_zero_markers=0)
        Team.objects.filter(id=team.id).update(action_points=0)

        messages.add_message(request, messages.INFO, "Hit an incident because the number of risks %d was more than the preventions %d." % (risks, preventions))
    else:
        Team.objects.filter(id=team.id).update(score=F('score') + (oil * 100))

        messages.add_message(request, messages.INFO, "Pumped %d units of oil." % oil)

    return HttpResponseRedirect(reverse('play'))
