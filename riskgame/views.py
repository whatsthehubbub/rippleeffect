from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django import forms

from django.db.models import F

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from django.views.decorators.http import require_POST

# from django.utils.translation import ugettext_lazy as _

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Field
# from crispy_forms.bootstrap import FormActions

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


@login_required
def team_detail(request, pk):
    t = loader.get_template('riskgame/team_detail.html')

    c = RequestContext(request, {
        'team': Team.objects.get(pk=pk),
        'title': "team"
    })

    return HttpResponse(t.render(c))

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
        "title": "profile"
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

            messages.add_message(request, messages.INFO, '<div class="form-success text-center">Profile updated successfully.</div>')

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
def notifications(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)

    t = loader.get_template('riskgame/notifications.html')

    c = RequestContext(request, {
        'notifications': Notification.objects.filter(team=teamplayer.team).order_by('-datecreated'),
        'title': 'messages'
    })

    return HttpResponse(t.render(c))


@login_required
def home(request):
    game = Game.objects.get_latest_game()

    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    
    if timezone.now() < game.start:
        # Pre game

        t = loader.get_template('riskgame/home-pregame.html')

        c = RequestContext(request, {
            'game': game
        })
    elif game.over():
        t = loader.get_template('riskgame/home-postgame.html')

        c = RequestContext(request, {
            'team': teamplayer.team
        })
    elif game.active():
        c = RequestContext(request, {
            'teammates': teamplayer.team.teamplayer_set.all(),
            'notifications': Notification.objects.filter(team=teamplayer.team).order_by('-datecreated')[:25],
            'title': "game"
        })

        if teamplayer.role == 'office':
            t = loader.get_template('riskgame/home-office.html')
        elif teamplayer.role == 'frontline':
            t = loader.get_template('riskgame/home-frontline.html')

            c['targetform'] = FrontLineForm(teamplayer)

        if teamplayer.show_game_start:
            TeamPlayer.objects.filter(pk=teamplayer.pk).update(show_game_start=False)

            if teamplayer.role == 'office':
                mt = loader.get_template('messages/start-game-office.html')
            elif teamplayer.role == 'frontline':
                mt = loader.get_template('messages/start-game-frontline.html')

            mc = RequestContext(request, {})
            messages.add_message(request, messages.INFO, mt.render(mc), extra_tags="modal")
        elif teamplayer.show_episode_start:
            TeamPlayer.objects.filter(pk=teamplayer.pk).update(show_episode_start=False)

            mt = loader.get_template('messages/start-episode.html')

            episode = EpisodeDay.objects.get(current=True).episode

            if episode.number != 1:
                previousEpisode = Episode.objects.get(number=episode.number-1)
                startDateTime = EpisodeDay.objects.filter(episode=previousEpisode).order_by('-end')[0].end
                endDateTime = EpisodeDay.objects.filter(episode=episode).order_by('-end')[0].end
                players = Player.objects.filter(notification__datecreated__gte=startDateTime, notification__datecreated__lte=endDateTime).distinct()
            else:
                players = []

            mc = RequestContext(request, {
                'episode': episode,
                'action_players': players
            })
            messages.add_message(request, messages.INFO, mt.render(mc), extra_tags="modal")
        elif teamplayer.show_turn_start:
            TeamPlayer.objects.filter(pk=teamplayer.pk).update(show_turn_start=False)

            turn = EpisodeDay.objects.get(current=True)

            if turn.number > 1 or turn.episode.number > 1:
                print 'here'
                previousTurn = EpisodeDay.objects.filter(end__lt=turn.end).order_by('-end')[0]

                startDateTime = previousTurn.end - (turn.end - previousTurn.end)
                endDateTime = previousTurn.end

                players = Player.objects.filter(notification__datecreated__gte=startDateTime, notification__datecreated__lte=endDateTime).distinct()
            else:
                players = []

            mt = loader.get_template('messages/start-turn.html')

            # Team events are returned for both roles
            mc = RequestContext(request, {
                'poorvision': teamplayer.team.is_event_active(Events.POOR_VISION),
                'tornado': teamplayer.team.is_event_active(Events.TORNADO),
                'highmarket': teamplayer.team.is_event_active(Events.HIGH_MARKET),
                'action_players': players
            })

            if teamplayer.role == 'office':
                # Add player specific events for office players
                mc['increasedrisk'] = teamplayer.is_event_active(Events.INCREASED_RISK)
                mc['lightning'] = teamplayer.is_event_active(Events.LIGHTNING)
                
            messages.add_message(request, messages.INFO, mt.render(mc), extra_tags="modal")
    
    c['startform'] = GameStartForm()

    return HttpResponse(t.render(c))

@login_required
def teams(request):
    t = loader.get_template('riskgame/teams.html')

    c = RequestContext(request, {
        'teams': Team.objects.all().order_by('-rank_points', '-pk'),
        'title': 'rankings'
    })

    return HttpResponse(t.render(c))

class GameStartForm(forms.Form):
    start = forms.DateTimeField(initial=timezone.now())
    turn_minutes = forms.IntegerField(initial=10)
    csv = forms.FileField(label="Teams and players (CSV)")

    def clean(self):
        cleaned_data = super(GameStartForm, self).clean()

        print cleaned_data

        import csv
        # print self.cleaned_data['csv']

        return cleaned_data

@login_required
def game_start(request):
    if request.method == 'POST':
        form = GameStartForm(request.POST, request.FILES)

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

            t = loader.get_template('messages/frontline-inspect-safety.html')

            c = RequestContext(request, {
                'resultnegative': [item for item in result if item == '0'],
                'resultpositive': [item for item in result if item == '1'],
                'unknowns': ['?'] * (8 - len(result)),
                'episode': EpisodeDay.objects.get(current=True).episode,
                'player': target.player,
                'poorvision': teamplayer.team.is_event_active(Events.POOR_VISION)
            })

            messages.add_message(request, messages.INFO, t.render(c))

            Notification.objects.create_frontline_safety_notification(teamplayer.team, player, target.player)
        else:
            t = loader.get_template('messages/out-of-actions.html')
            c = RequestContext(request, {})
            messages.add_message(request, messages.INFO, t.render(c))

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

            t = loader.get_template('messages/frontline-predict-event.html')

            c = RequestContext(request, {
                'episode': EpisodeDay.objects.get(current=True).episode,
                'player': target.player,
                'event': event
            })

            Notification.objects.create_frontline_event_notification(teamplayer.team, player, target.player)

            messages.add_message(request, messages.INFO, t.render(c))
        else:
            t = loader.get_template('messages/out-of-actions.html')
            c = RequestContext(request, {})
            messages.add_message(request, messages.INFO, t.render(c))

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

            # result += (8-len(result)) * ['?']

            if pile == 'gather':
                Notification.objects.create_inspected_production_notification(team, player)

                t = loader.get_template('messages/office-inspect-production.html')
            elif pile == 'risk':
                Notification.objects.create_inspected_safety_notification(team, player)

                t = loader.get_template('messages/office-inspect-safety.html')

            c = RequestContext(request, {
                'resultnegative': [item for item in result if item == '0'],
                'resultpositive': [item for item in result if item == '1'],
                'unknowns': ['?'] * (8 - len(result)),
                'episode': EpisodeDay.objects.get(current=True).episode,
                'player': player,
                'poorvision': team.is_event_active(Events.POOR_VISION)
            })

            messages.add_message(request, messages.INFO, t.render(c))
    else:
        t = loader.get_template('messages/out-of-actions.html')
        c = RequestContext(request, {})
        messages.add_message(request, messages.INFO, t.render(c))

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

                t = loader.get_template('messages/office-improve-production.html')
            elif pile == 'risk':
                Notification.objects.create_improved_safety_notification(team, player)

                t = loader.get_template('messages/office-improve-safety.html')

            c = RequestContext(request, {
                'episode': EpisodeDay.objects.get(current=True).episode,
                'player': player
            })

            messages.add_message(request, messages.INFO, t.render(c))

    else:
        t = loader.get_template('messages/out-of-actions.html')
        c = RequestContext(request, {})
        messages.add_message(request, messages.INFO, t.render(c))

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

        t = loader.get_template('messages/office-plan-production.html')

        c = RequestContext(request, {
            'episode': EpisodeDay.objects.get(current=True).episode,
            'player': player
        })

        messages.add_message(request, messages.INFO, t.render(c))
    else:
        t = loader.get_template('messages/out-of-actions.html')
        c = RequestContext(request, {})
        messages.add_message(request, messages.INFO, t.render(c))

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

        t = loader.get_template('messages/office-place-barrier.html')

        c = RequestContext(request, {
            'episode': EpisodeDay.objects.get(current=True).episode,
            'player': player
        })

        messages.add_message(request, messages.INFO, t.render(c))
    else:
        t = loader.get_template('messages/out-of-actions.html')
        c = RequestContext(request, {})
        messages.add_message(request, messages.INFO, t.render(c))

    return HttpResponseRedirect(reverse('home'))

@login_required
def play_pump(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    # This is horrible but it works
    resource_count, production, incident_count, safety, barrier_count = teamplayer.pump()
    teamplayer.save()

    t = loader.get_template('messages/office-produce-resources.html')

    c = RequestContext(request, {
        'episode': EpisodeDay.objects.get(current=True).episode,
        'player': player,
        'resource_count': resource_count,
        'production': production,
        'incident_count': incident_count,
        'safety': safety,
        'barrier_count': barrier_count,
        'tornado': team.is_event_active(Events.TORNADO),
        'highmarket': team.is_event_active(Events.HIGH_MARKET)
    })

    if incident_count > barrier_count:
        # We have an incident
        Team.objects.filter(pk=team.pk).update(goal_zero_streak=team.get_goal_zero_streak())
        Team.objects.filter(pk=team.pk).update(goal_zero_markers=0)

        # Lose all your action points if the hard wind event is active
        if team.is_event_active(Events.TORNADO):
            Team.objects.filter(pk=team.pk).update(action_points=0)

        Notification.objects.create_retrieved_failure_notification(team, player)
    else:
        high_market_modifier = 1
        if team.is_event_active(Events.HIGH_MARKET):
            high_market_modifier = 2

        points_scored = team.goal_zero_markers * resource_count * high_market_modifier * 100

        Team.objects.filter(pk=team.pk).update(resources_collected=F('resources_collected') + resource_count)
        Team.objects.filter(pk=team.pk).update(resources_collected_episode=F('resources_collected_episode') + resource_count)

        Team.objects.filter(pk=team.pk).update(victory_points=F('victory_points') + points_scored)

        # Rank points are derived from victory points
        Team.objects.filter(pk=team.pk).update(rank_points=F('victory_points') / team.get_office_players().count())
        Team.objects.get(pk=team.pk).update_rank()
        
        Team.objects.filter(pk=team.pk).update(victory_points_episode=F('victory_points_episode') + points_scored)

        Notification.objects.create_retrieved_success_notification(team, player, resource_count, points_scored)

    messages.add_message(request, messages.INFO, t.render(c))

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
