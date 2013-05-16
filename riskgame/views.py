import itertools

from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext, loader
from django.template.loader import render_to_string

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django import forms

from django.db.models import F, Q

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.sites.models import get_current_site

from django.shortcuts import render, render_to_response, redirect

from django.views.decorators.http import require_POST

# from django.utils.translation import ugettext_lazy as _

from riskgame.models import *
from riskgame.tasks import change_days, invite_user

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    else:
        return render_to_response('riskgame/index.html', {}, context_instance=RequestContext(request))


# def pre_launch(request):
#     t = loader.get_template('riskgame/pre_launch.html')

#     c = RequestContext(request, {
#         'game': Game.objects.get_latest_game()
#     })

#     return HttpResponse(t.render(c))


class CreateTeamform(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', )

    # def __init__(self, *args, **kwargs):
    #     self.helper = FormHelper()

    #     self.helper.form_class = 'form'
    #     self.helper.form_action = reverse('team_create')
    #     self.helper.form_method = 'post'

    #     self.helper.layout = Layout(
    #         Field('name', css_class='input-block-level', placeholder='Name'),
    #         FormActions(
    #             Submit('submit', _('Send'), css_class='btn')
    #         )
    #     )

    #     super(CreateTeamform, self).__init__(*args, **kwargs)

@login_required
@require_POST
def team_create(request):
    name = request.POST.get('name', '')

    player = request.user.get_or_create_player()
    team = Team.objects.create(name=name, leader=player)

    TeamPlayer.objects.create(player=player, team=team)

    return HttpResponseRedirect(reverse('team_detail', args=[team.pk]))


@login_required
def team_detail(request, pk):
    team = Team.objects.get(pk=pk)

    return render_to_response('riskgame/team_detail.html', {
        'team': team,
        'title': "team",
        'join_requests': TeamJoinRequest.objects.filter(team=team, invite=False, accepted=False, rejected=False).order_by('-datecreated'),
        'pending_requests': TeamJoinRequest.objects.filter(team=team, invite=False, accepted=True).order_by('-datedecided'),
        'denied_requests': TeamJoinRequest.objects.filter(team=team, invite=False, rejected=True)
    }, context_instance=RequestContext(request))

@login_required
def team_leave(request):
    if request.method == "POST":
        player = request.user.get_or_create_player()
        teamplayer = TeamPlayer.objects.get(player=player)

        teamplayer.delete()

        return redirect(reverse('home'))
    else:
        return render_to_response('riskgame/team_leave.html', {

        }, context_instance=RequestContext(request))

@login_required
@require_POST
def team_kick(request):
    playerid = request.POST.get('playerid', '')

    if playerid:
        player = Player.objects.get(pk=playerid)
        teamplayer = TeamPlayer.objects.get(player=player)
        team = teamplayer.team

        teamplayer.delete()

        return redirect(reverse('team_detail', args=[team.pk]))

@login_required
@require_POST
def request_team_join(request, pk):
    player = request.user.get_or_create_player()
    team = Team.objects.get(pk=pk)

    TeamJoinRequest.objects.create(team=team, player=player)

    return HttpResponseRedirect(reverse('team_detail', args=[team.pk]))

@login_required
@require_POST
def accept_team_join(request, pk):
    join_request = TeamJoinRequest.objects.get(pk=request.POST.get('tjr_id'))

    # The player doing the accepting, NOT the player being accepted
    player = request.user.get_or_create_player()

    try:
        # Permission check if the player doing this is a member of the team of the request
        TeamPlayer.objects.get(player=player, team=join_request.team)

        join_request.accepted = True
        join_request.datedecided = timezone.now()
        join_request.save()

        subject = render_to_string('emails/accepted_subject.txt', {
            'site': get_current_site(request)
        })
        subject = ''.join(subject.splitlines())

        body = render_to_string('emails/accepted_body.txt', {
            'site': get_current_site(request),
            'team': join_request.team
        })

        join_request.player.user.email_user(subject, body)

        messages.add_message(request, messages.INFO, '<div class="form-success text-center">Team join request accepted.</div>')

        return HttpResponseRedirect(reverse('team_detail', args=[join_request.team.pk]))
    except TeamPlayer.DoesNotExist:
        pass

@login_required
@require_POST
def reject_team_join(request, pk):
    join_request = TeamJoinRequest.objects.get(pk=request.POST.get('tjr_id'))

    player = request.user.get_or_create_player()

    try:
        # Permission check if the player doing this is a member of the team of the request
        TeamPlayer.objects.get(player=player, team=join_request.team)

        join_request.rejected = True
        join_request.datedecided = timezone.now()
        join_request.save()

        subject = render_to_string('emails/rejected_subject.txt', {
            'site': get_current_site(request)
        })
        subject = ''.join(subject.splitlines())

        body = render_to_string('emails/rejected_body.txt', {
            'site': get_current_site(request),
            'team': join_request.team
        })

        join_request.player.user.email_user(subject, body)

        messages.add_message(request, messages.INFO, '<div class="form-success text-center">Team join request declined.</div>')

        return HttpResponseRedirect(reverse('team_detail', args=[join_request.team.pk]))
    except TeamPlayer.DoesNotExist:
        pass


@login_required
@require_POST
def confirm_team_join(request, pk):
    join_request = TeamJoinRequest.objects.get(pk=request.POST.get('tjr_id'))

    player = request.user.get_or_create_player()

    try:
        TeamPlayer.objects.get(player=player, team=join_request.team)

        # This player is already a member of this team
        # something that should not happen
    except TeamPlayer.DoesNotExist:
        # Confirm this player joining this team
        role = request.POST.get('role', 'office')

        TeamPlayer.objects.create(player=player, team=join_request.team, role=role)

        messages.add_message(request, messages.INFO, '<div class="form-success text-center">You are now a member of team %s.</div>' % join_request.team.name)

    return HttpResponseRedirect(reverse('home'))

@login_required
@require_POST
def reconsider_team_join(request, pk):
    """Method where somebody accepted into a team doesn't actually want to confirm. Also used to reject invitations."""
    join_request = TeamJoinRequest.objects.get(pk=request.POST.get('tjr_id'))
    join_request.delete()

    messages.add_message(request, messages.INFO, '<div class="form-success text-center">Request elided.</div>')

    return HttpResponseRedirect(reverse('home'))


@login_required
def team_your(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)

    return HttpResponseRedirect(reverse('team_detail', args=[teamplayer.team.pk]))


@login_required
def players(request):
    players = Player.objects.all().order_by('name', 'user__email')

    query = request.GET.get('s', '')

    if query:
        players = players.filter(Q(name__icontains=query) | Q(user__email__icontains=query))

    page = request.GET.get('page', '')

    paginator = Paginator(players, 50)
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)

    return render_to_response('riskgame/players.html', {
        'players': players
    }, context_instance=RequestContext(request))

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
        'profileform': profileform,
        "title": "profile"
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

    nots = Notification.objects.filter(team=teamplayer.team).order_by('-datecreated')
    paginator = Paginator(nots, 50)

    page = request.GET.get('page')

    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)

    if not request.is_ajax():
        t = loader.get_template('riskgame/notifications.html')

        c = RequestContext(request, {
            'notifications': notifications,
            'title': 'messages'
        })

        return HttpResponse(t.render(c))
    else:
        t = loader.get_template('partials/notification.html')

        return HttpResponse('\n'.join([t.render(RequestContext(request, {'notification': n})) for n in notifications]))

@login_required
def how_to_play(request):
    return render_to_response('riskgame/how-to-play.html', {}, context_instance=RequestContext(request))

@login_required
def home(request):
    game = Game.objects.get_latest_game()

    player = request.user.get_or_create_player()

    member_of_a_team = False

    try:
        teamplayer = TeamPlayer.objects.get(player=player)

        member_of_a_team = True
    except TeamPlayer.DoesNotExist:
        member_of_a_team = False

    # TODO What to do about people without a team after the game has started?

    if timezone.now() < game.start:
        # Pre game
        if member_of_a_team:
            t = loader.get_template('riskgame/home-pregame.html')

            c = RequestContext(request, {
                'game': game
            })
        else:
            # Show home alone only for people before the game starts
            t = loader.get_template('riskgame/home-alone.html')

            c = RequestContext(request, {
                'teamform': CreateTeamform(),
                'accepted_requests': TeamJoinRequest.objects.filter(accepted=True, confirmed=False).order_by('-datedecided')
            })
    elif game.over():
        t = loader.get_template('riskgame/home-postgame.html')

        c = RequestContext(request, {
            'team': teamplayer.team
        })
    elif game.active():
        c = RequestContext(request, {
            'teammates': teamplayer.team.teamplayer_set.all(),
            'notifications': Notification.objects.filter(team=teamplayer.team).order_by('-datecreated')[:15],
            'title': "game"
        })

        if teamplayer.role == 'office':
            t = loader.get_template('riskgame/home-office.html')
        elif teamplayer.role == 'frontline':
            t = loader.get_template('riskgame/home-frontline.html')

            c['targetform'] = FrontLineForm(teamplayer)

        if teamplayer.show_game_start:
            if teamplayer.role == 'office':
                mt = loader.get_template('messages/start-game-office.html')
            elif teamplayer.role == 'frontline':
                mt = loader.get_template('messages/start-game-frontline.html')

            mc = RequestContext(request, {})
            messages.add_message(request, messages.INFO, mt.render(mc), extra_tags="modal")
        elif teamplayer.show_episode_start:
            mt = loader.get_template('messages/start-episode.html')

            episode = EpisodeDay.objects.get(current=True).episode

            if episode.number != 1:
                previousEpisode = Episode.objects.get(number=episode.number-1)
                startDateTime = EpisodeDay.objects.filter(episode=previousEpisode).order_by('-end')[0].end
                endDateTime = EpisodeDay.objects.filter(episode=episode).order_by('-end')[0].end
                players = Player.objects.filter(notification__datecreated__gte=startDateTime, notification__datecreated__lte=endDateTime, notification__action=True, notification__team=teamplayer.team).distinct()
            else:
                players = []

            mc = RequestContext(request, {
                'episode': episode,
                'action_players': players
            })
            messages.add_message(request, messages.INFO, mt.render(mc), extra_tags="modal")
        elif teamplayer.show_turn_start:
            turn = EpisodeDay.objects.get(current=True)

            if turn.number > 1 or turn.episode.number > 1:
                previousTurn = EpisodeDay.objects.filter(end__lt=turn.end).order_by('-end')[0]

                startDateTime = previousTurn.end - (turn.end - previousTurn.end)
                endDateTime = previousTurn.end

                players = Player.objects.filter(notification__datecreated__gte=startDateTime, notification__datecreated__lte=endDateTime, notification__action=True, notification__team=teamplayer.team).distinct()
            else:
                players = []

            mt = loader.get_template('messages/start-turn.html')

            # Team events are returned for both roles
            mc = RequestContext(request, {
                'event': teamplayer.get_event_for_day(turn),
                'lightninghit': teamplayer.lightning_hit,
                'action_players': players
            })
                
            messages.add_message(request, messages.INFO, mt.render(mc), extra_tags="modal")

    return HttpResponse(t.render(c))

@login_required
def message_seen(request, message):
    # TODO should be post
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)

    if message == 'game':
        TeamPlayer.objects.filter(pk=teamplayer.pk).update(show_game_start=False)
    elif message == 'episode':
        TeamPlayer.objects.filter(pk=teamplayer.pk).update(show_episode_start=False)
    elif message == 'turn':
        TeamPlayer.objects.filter(pk=teamplayer.pk).update(show_turn_start=False)

    return HttpResponseRedirect(reverse('home'))

@login_required
def message_unseen(request, message):
    # TODO should be post
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)

    if message == 'game':
        TeamPlayer.objects.filter(pk=teamplayer.pk).update(show_game_start=True)
    elif message == 'episode':
        TeamPlayer.objects.filter(pk=teamplayer.pk).update(show_episode_start=True)
    elif message == 'turn':
        TeamPlayer.objects.filter(pk=teamplayer.pk).update(show_turn_start=True)

    return HttpResponseRedirect(reverse('home'))

@login_required
def teams(request):
    t = loader.get_template('riskgame/teams.html')

    c = RequestContext(request, {
        'teams': Team.objects.all().order_by('-rank_points', '-pk'),
        'title': 'rankings'
    })

    return HttpResponse(t.render(c))

class GameStartForm(forms.Form):
    start = forms.DateTimeField(initial=timezone.now)
    turn_minutes = forms.IntegerField(initial=10)
    csv = forms.FileField(label="Teams and players (CSV)", required=False)

    def clean(self):
        cleaned_data = super(GameStartForm, self).clean()

        if cleaned_data['csv']:
            try:
                import csv, StringIO
                from email.utils import parseaddr

                content = StringIO.StringIO(cleaned_data['csv'].read())

                reader = csv.reader(content)

                players = []

                for row in reader:
                    team_name = row[0]
                    email = parseaddr(row[1])[1]

                    if not email[1]:
                        raise forms.ValidationError("Passed value %s is not a valid e-mail address." % row[1])

                    role = row[2]

                    if role not in ['office', 'frontline']:
                        raise forms.ValidationError("Role for %s did not conform to 'frontline' or 'office'." % email)

                    alias = row[3]

                    players.append((team_name, email, role, alias))
            except:
                raise forms.ValidationError("Did not receive a valid CSV file.")

            # Check for e-mail duplicates
            for player in players:
                email = player[1]

                if len([p for p in players if p[1] == email]) > 1:
                    raise forms.ValidationError("Received a duplicate for e-mail: %s" % email)

            # Stuff the parsed player array in cleaned_data
            cleaned_data['players'] = players
        else:
            cleaned_data['players'] = []

        return cleaned_data

@login_required
@user_passes_test(lambda u: u.is_admin)
def game_start(request):
    if request.method == 'POST':
        startform = GameStartForm(request.POST, request.FILES)

        if startform.is_valid():
            minutes = startform.cleaned_data.get('turn_minutes', 10)
            start = startform.cleaned_data.get('start', timezone.now())
            players = startform.cleaned_data.get('players', [])

            logger.info("Starting a game of %d minutes starting on %s", minutes, str(start))

            if players:
                # TODO this has probably got to go
                logger.info("Starting game with players passed.")

                # Delete all non admin users
                EmailUser.objects.exclude(is_admin=True).delete()
                
                Player.objects.all().delete()
                Team.objects.all().delete()
                TeamPlayer.objects.all().delete()

                for player in players:
                    team_name = player[0]
                    email = player[1]
                    role = player[2]
                    alias = player[3]

                    logger.info("Creating player %s %s with role %s in team %s", alias, email, role, team_name)

                    user = EmailUser.objects.create_user(email=email)

                    # Put e-mail inviting this user in the queue
                    invite_user.delay(user, get_current_site(request))

                    player, player_created = Player.objects.get_or_create(user=user, name=alias)

                    team, team_created = Team.objects.get_or_create(name=team_name)

                    TeamPlayer.objects.get_or_create(player=player, team=team, role=role)

                Game.objects.get_latest_game().initialize(start=start, dayLengthInMinutes=minutes)

                logout(request)
            else:
                logger.info("Starting game without players passed.")

                # Starting a game with current team and players, so reset stats
                Team.objects.all().update(goal_zero_markers=0)
                Team.objects.all().update(goal_zero_streak=1)
                Team.objects.all().update(action_points=0)
                Team.objects.all().update(frontline_action_points=0)
                Team.objects.all().update(rank_points=0)
                Team.objects.all().update(victory_points=0)
                Team.objects.all().update(victory_points_episode=0)
                Team.objects.all().update(resources_collected=0)
                Team.objects.all().update(resources_collected_episode=0)
                Team.objects.all().update(active_events='')

                TeamPlayer.objects.all().update(gather_pile='')
                TeamPlayer.objects.all().update(gather_markers=0)
                TeamPlayer.objects.all().update(risk_pile='')
                TeamPlayer.objects.all().update(prevent_markers=0)
                TeamPlayer.objects.all().update(episode_events='')
                TeamPlayer.objects.all().update(active_events='')

                Game.objects.get_latest_game().initialize(start=start, dayLengthInMinutes=minutes)

                for team in Team.objects.all():
                    team.update_rank()

            change_days()

            return HttpResponseRedirect(reverse('home'))
    else:
        startform = GameStartForm()

    return render(request, 'riskgame/start_new_game.html', {
        'startform': startform
    })

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
            messages.add_message(request, messages.INFO, t.render(c), extra_tags="brief")

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
            messages.add_message(request, messages.INFO, t.render(c), extra_tags="brief")

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
        messages.add_message(request, messages.INFO, t.render(c), extra_tags="brief")

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

            messages.add_message(request, messages.INFO, t.render(c), extra_tags="brief")

    else:
        t = loader.get_template('messages/out-of-actions.html')
        c = RequestContext(request, {})
        messages.add_message(request, messages.INFO, t.render(c), extra_tags="brief")

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

        messages.add_message(request, messages.INFO, t.render(c), extra_tags="brief")
    else:
        t = loader.get_template('messages/out-of-actions.html')
        c = RequestContext(request, {})
        messages.add_message(request, messages.INFO, t.render(c), extra_tags="brief")

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

        messages.add_message(request, messages.INFO, t.render(c), extra_tags="brief")
    else:
        t = loader.get_template('messages/out-of-actions.html')
        c = RequestContext(request, {})
        messages.add_message(request, messages.INFO, t.render(c), extra_tags="brief")

    return HttpResponseRedirect(reverse('home'))


@login_required
def play_confirm_pump(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    t = loader.get_template('messages/office-confirm-production.html')

    c = RequestContext(request, {
        'episode': EpisodeDay.objects.get(current=True).episode,
        'player': player,
        'tornado': team.is_event_active(Events.TORNADO),
        'highmarket': team.is_event_active(Events.HIGH_MARKET)
    })

    messages.add_message(request, messages.INFO, t.render(c))

    return HttpResponseRedirect(reverse('home'))

@login_required
def play_pump(request):
    player = request.user.get_or_create_player()
    teamplayer = TeamPlayer.objects.get(player=player)
    team = teamplayer.team

    # This is horrible but it works
    resource_count, production, incident_count, safety, barrier_count, gather_count = teamplayer.pump()
    teamplayer.save()

    t = loader.get_template('messages/office-produce-resources.html')

    c = RequestContext(request, {
        'episode': EpisodeDay.objects.get(current=True).episode,
        'player': player,
        'resource_count': resource_count,
        'production': production,
        'production_draws': len(list(itertools.chain(*production))),
        'incident_count': incident_count,
        'safety': safety,
        'risk_draws': len(list(itertools.chain(*safety))),
        'barrier_count': barrier_count,
        'gather_count': gather_count,
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

        c['base_points'] = resource_count * 100
        c['goal_zero'] = team.goal_zero_markers
        c['points'] = points_scored

        Team.objects.filter(pk=team.pk).update(resources_collected=F('resources_collected') + resource_count)
        Team.objects.filter(pk=team.pk).update(resources_collected_episode=F('resources_collected_episode') + resource_count)

        Team.objects.filter(pk=team.pk).update(victory_points=F('victory_points') + points_scored)

        # Rank points are derived from victory points
        Team.objects.filter(pk=team.pk).update(rank_points=F('victory_points') / team.get_office_players().count())
        Team.objects.get(pk=team.pk).update_rank()
        
        Team.objects.filter(pk=team.pk).update(victory_points_episode=F('victory_points_episode') + points_scored)
        Team.objects.filter(pk=team.pk).update(victory_points_turn=F('victory_points_turn') + points_scored)

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
