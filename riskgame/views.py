from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django import forms

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


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    t = loader.get_template('riskgame/index.html')

    c = RequestContext(request, {
    })

    return HttpResponse(t.render(c))


# def pre_launch(request):
#     t = loader.get_template('riskgame/pre_launch.html')

#     c = RequestContext(request, {
#         'game': Game.objects.get_latest_game()
#     })

#     return HttpResponse(t.render(c))


# class CreateTeamform(forms.ModelForm):
#     class Meta:
#         model = Team
#         fields = ('name', )

#     def __init__(self, *args, **kwargs):
#         self.helper = FormHelper()

#         self.helper.form_class = 'form'
#         self.helper.form_action = reverse('team_create')
#         self.helper.form_method = 'post'

#         self.helper.layout = Layout(
#             Field('name', css_class='input-block-level', placeholder='Name'),
#             FormActions(
#                 Submit('submit', _('Send'), css_class='btn')
#             )
#         )

#         super(CreateTeamform, self).__init__(*args, **kwargs)

# @login_required
# def team_create(request):
#     if request.method == "POST":
#         name = request.POST.get('name', '')

#         player = request.user.get_or_create_player()
#         Team.objects.create(name=name, leader=player)

#         return HttpResponseRedirect(reverse('index'))


class TeamDetail(DetailView):
    model = Team
    template_name = 'riskgame/team_detail.html'
    context_object_name = 'team'

# @login_required
# @require_POST
# def request_team_join(request, pk):
#     player = request.user.get_or_create_player()
#     team = Team.objects.get(id=pk)

#     TeamJoinRequest.objects.create(team=team, player=player)

#     return HttpResponseRedirect(reverse('team_detail', args=[player.team.id]))

# @login_required
# @require_POST
# def accept_team_join(request, pk):
#     join_request = TeamJoinRequest.objects.get(id=request.POST.get('join_request_id', ''))

#     print join_request

#     print request.user.get_or_create_player()
#     print join_request.team.leader

#     if request.user.get_or_create_player() == join_request.team.leader:
#         player = join_request.player
#         player.team = join_request.team
#         player.save()

#         join_request.delete()

#         return HttpResponseRedirect(reverse('team_detail', args=[player.team.id]))

@login_required
def team_your(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)

    return HttpResponseRedirect(reverse('team_detail', args=[teamplayer.team.pk]))


@login_required
def players(request):
    t = loader.get_template('riskgame/players.html')

    c = RequestContext(request, {
        'players': Player.objects.all()
    })

    return HttpResponse(t.render(c))

def player_profile(request, pk):
    player = Player.objects.get(pk=pk)

    t = loader.get_template('riskgame/player_profile.html')

    c = RequestContext(request, {
        'player': player,
        'teamplayer': TeamPlayer.objects.get(player=player)
    })

    return HttpResponse(t.render(c))

def player_profile_own(request):
    player = request.user.get_or_create_player()

    return HttpResponseRedirect(reverse('player_profile', args=[player.pk]))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'receive_email')

def player_profile_edit(request):
    t = loader.get_template('riskgame/player_profile_edit.html')

    player = request.user.get_or_create_player()

    if request.method == "POST":
        profileform = ProfileForm(request.POST, instance=player)

        if profileform.is_valid():
            profileform.save()

            return HttpResponseRedirect(reverse('player_profile_own'))
    else:
        profileform = ProfileForm(instance=player)

    c = RequestContext(request, {
        'profileform': profileform
    })

    return HttpResponse(t.render(c))

class FrontLineForm(forms.Form):
    def __init__(self, teamplayer, *args, **kwargs):
        super(FrontLineForm, self).__init__(*args, **kwargs)

        self.fields['target'] = forms.ModelChoiceField(queryset=teamplayer.team.teamplayer_set.filter(role='office'))

@login_required
def home(request):
    game = Game.objects.get_latest_game()

    if timezone.now() < game.start:
        # Pre game

        t = loader.get_template('riskgame/home-pregame.html')

        c = RequestContext(request, {
            'game': game
        })

    if game.over():
        t = loader.get_template('riskgame/home-postgame.html')

        c = RequestContext(request, {
            
        })

    if game.active():
        player = request.user.get_or_create_player()
        teamplayer = TeamPlayer.objects.get(player=player)

        c = RequestContext(request, {
            'teamplayer': teamplayer,
            'teammates': teamplayer.team.teamplayer_set.all(),
            'currentDay': EpisodeDay.objects.get(current=True),
            'notifications': Notification.objects.filter(team=teamplayer.team).order_by('-datecreated')[:25],
        })

        if teamplayer.role == 'office':
            t = loader.get_template('riskgame/home-office.html')
        elif teamplayer.role == 'frontline':
            t = loader.get_template('riskgame/home-frontline.html')

            c['targetform'] = FrontLineForm(teamplayer)

    c['startform'] = GameStartForm()

    return HttpResponse(t.render(c))

@login_required
def teams(request):
    t = loader.get_template('riskgame/teams.html')

    c = RequestContext(request, {
        'teams': Team.objects.all()
    })

    return HttpResponse(t.render(c))

class GameStartForm(forms.Form):
    turn_minutes = forms.IntegerField(initial=10)

@login_required
def game_start(request):
    if request.method == 'POST':
        form = GameStartForm(request.POST)

        if form.is_valid():
            minutes = form.cleaned_data.get('turn_minutes', 10)

            Game.objects.get_latest_game().initialize(dayLengthInMinutes=minutes)

            from riskgame.tasks import change_days
            change_days()

    return HttpResponseRedirect(reverse('home'))

# Frontline actions

@login_required
@require_POST
def inspect_risks(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)

    form = FrontLineForm(teamplayer, request.POST)

    if form.is_valid():
        if Team.objects.filter(pk=teamplayer.team.pk, frontline_action_points__gt=0).update(frontline_action_points=F('frontline_action_points')-1):
            target = form.cleaned_data.get('target')

            result = target.inspect('risk')

            result += (8-len(result)) * ['?']

            Notification.objects.create_frontline_safety_notification(teamplayer.team, player)

            messages.add_message(request, messages.INFO, "Inspected risk for player %s and found: %s" % (str(target.player), ' '.join(result)))

    return HttpResponseRedirect(reverse('home'))


@login_required
@require_POST
def inspect_event(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)

    form = FrontLineForm(teamplayer, request.POST)

    if form.is_valid():
        if Team.objects.filter(pk=teamplayer.team.pk, frontline_action_points__gt=0).update(frontline_action_points=F('frontline_action_points')-1):
            target = form.cleaned_data.get('target')

            # Get next event
            currentDay = EpisodeDay.objects.get(current=True)
            event = target.get_event_for_day(currentDay.next)

            Notification.objects.create_frontline_event_notification(teamplayer.team, player)

            messages.add_message(request, messages.INFO, "Inspected event for player %s and found: %s" % (str(target.player), event))
    return HttpResponseRedirect(reverse('home'))


# Office actions

@login_required
def play_inspect(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    if Team.objects.filter(pk=team.pk, action_points__gt=0).update(action_points=F('action_points')-1):
        pile = request.POST.get('pile', '')

        if pile:
            result = teamplayer.inspect(pile)
            teamplayer.save()

            result += (8-len(result)) * ['?']

            if pile == 'gather':
                Notification.objects.create_inspected_production_notification(team, player)
            elif pile == 'risk':
                Notification.objects.create_inspected_safety_notification(team, player)

            # TODO remove these messages
            messages.add_message(request, messages.INFO, "Inspected %s and found: %s" % (pile, ' '.join(result)))

    return HttpResponseRedirect(reverse('home'))


@login_required
def play_invest(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    if Team.objects.filter(pk=team.pk, action_points__gt=0).update(action_points=F('action_points')-1):
        pile = request.POST.get('pile', '')

        if pile:
            teamplayer.invest(pile)
            teamplayer.save()

            if pile == 'gather':
                Notification.objects.create_improved_production_notification(team, player)
            elif pile == 'risk':
                Notification.objects.create_improved_safety_notification(team, player)

            # Add message
            messages.add_message(request, messages.INFO, "Invested in pile %s" % pile)

    return HttpResponseRedirect(reverse('home'))


@login_required
def play_gather(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    if Team.objects.filter(pk=team.pk, action_points__gt=0).update(action_points=F('action_points')-1):
        teamplayer.gather()
        teamplayer.save()

        Notification.objects.create_gather_notification(team, player)

        messages.add_message(request, messages.INFO, "Placed gather token.")

    return HttpResponseRedirect(reverse('home'))

@login_required
def play_prevent(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    if Team.objects.filter(pk=team.pk, action_points__gt=0).update(action_points=F('action_points')-1):
        teamplayer.prevent()
        teamplayer.save()

        Notification.objects.create_prevent_notification(team, player)

        messages.add_message(request, messages.INFO, "Placed prevent token.")

    return HttpResponseRedirect(reverse('home'))

@login_required
def play_pump(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    oil, risks, preventions = teamplayer.pump()
    teamplayer.save()

    if risks > preventions:
        # We have an incident
        Team.objects.filter(pk=team.pk).update(goal_zero_markers=0)

        # Lose all your action points if the hard wind event is active
        if team.is_event_active(Events.HARD_WIND):
            Team.objects.filter(pk=team.pk).update(action_points=0)

        Notification.objects.create_retrieved_failure_notification(team, player)

        messages.add_message(request, messages.INFO, "Hit an incident because the number of risks %d was more than the preventions %d." % (risks, preventions))
    else:
        high_market_modifier = 1
        if team.is_event_active(Events.HIGH_MARKET):
            high_market_modifier = 2

        points_scored = team.goal_zero_markers * oil * high_market_modifier * 100

        Team.objects.filter(pk=team.pk).update(resources_collected=F('resources_collected') + oil)
        Team.objects.filter(pk=team.pk).update(resources_collected_episode=F('resources_collected_episode') + oil)

        Team.objects.filter(pk=team.pk).update(victory_points=F('victory_points') + points_scored)
        Team.objects.filter(pk=team.pk).update(victory_points_episode=F('victory_points_episode') + points_scored)

        Notification.objects.create_retrieved_success_notification(team, player, oil, points_scored)

        messages.add_message(request, messages.INFO, "Pumped %d units of oil." % oil)

    return HttpResponseRedirect(reverse('home'))


def player_unsubscribe(request, h):
    try:
        player = Player.objects.get(emails_unsubscribe_hash=h)

        player.receive_email = False
        player.update_unsubscribe_hash()

        player.save()

        logging.info("Unsubscribed player %s from further e-mails." % player.email())
    except:
        logging.error("Player with hash %s does not exist to unsubscribe", h)

    # TODO put a unsubscribe succesful template here

    return HttpResponseRedirect(reverse('index'))
