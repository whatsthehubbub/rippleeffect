from django.db import models
from django.db.models import F

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail

from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.template.loader import render_to_string

import random
import datetime
import math
import hashlib, hmac

import logging
logger = logging.getLogger('ripple')


# Events have integer values
# 0 = No event
# 1 = Poor vision, team
# 2 = Tornado, team
# 3 = High market, team
# 4 = Increased risk, player
# 5 = Lightning, player

def enum(**enums):
    enums = dict(enums)
    rev = dict((value, key) for key, value in enums.iteritems())
    enums['reverse'] = rev

    return type('Enum', (), enums)

Events = enum(NO_EVENT='0', POOR_VISION='1', TORNADO='2', HIGH_MARKET='3', INCREASED_RISK='4', LIGHTNING='5')


class EmailUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=EmailUserManager.normalize_email(email)
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save()

        return user


class EmailUser(AbstractBaseUser):
    email = models.EmailField(verbose_name=_('E-mail address'), max_length=255, unique=True, db_index=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def send_invitation_email(self, site):
        """Send an invitation email to the user with a new password."""
        
        password = EmailUser.objects.make_random_password()
        
        self.set_password(password)
        self.save()

        ctx_dict = {
            'site': site,
            'password': password
        }

        subject = render_to_string('registration/invitation_email_subject.txt',
                                   ctx_dict)
        
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('registration/invitation_email.txt',
                                   ctx_dict)
        
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def get_or_create_player(self):
        try:
            return Player.objects.get(user=self)
        except Player.DoesNotExist:
            return Player.objects.create(user=self)


class ValidEmailDomain(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


from django.core.mail import EmailMessage

class NotificationManager(models.Manager):
    # Inspect frontline notifications
    def create_frontline_safety_notification(self, team, player, target):
        return Notification.objects.create(identifier='frontline-safety', team=team, player=player, target=target)

    def create_frontline_event_notification(self, team, player, target):
        return Notification.objects.create(identifier='frontline-event', team=team, player=player, target=target)

    # Inspect notifications
    def create_inspected_safety_notification(self, team, player):
        return Notification.objects.create(identifier='player-inspected-safety', team=team, player=player)

    def create_inspected_production_notification(self, team, player):
        return Notification.objects.create(identifier='player-inspected-production', team=team, player=player)

    # Event notifications
    def create_received_poorvision_event_notification(self, team, player):
        return Notification.objects.create(identifier='player-received-poorvision-event', team=team, player=player, action=False)
    
    def create_received_tornado_event_notification(self, team, player):
        return Notification.objects.create(identifier='player-received-tornado-event', team=team, player=player, action=False)
    
    def create_received_highmarket_event_notification(self, team, player):
        return Notification.objects.create(identifier='player-received-highmarket-event', team=team, player=player, action=False)

    def create_received_increasedrisk_event_notification(self, team, player):
        return Notification.objects.create(identifier='player-received-increasedrisk-event', team=team, player=player, action=False)

    def create_received_lightning_event_notification(self, team, player):
        return Notification.objects.create(identifier='player-received-lightning-event', team=team, player=player, action=False)

    # Improvement notifications
    def create_improved_safety_notification(self, team, player):
        return Notification.objects.create(identifier='player-improved-safety', team=team, player=player)

    def create_improved_production_notification(self, team, player):
        return Notification.objects.create(identifier='player-improved-production', team=team, player=player)

    # Place marker notifications
    def create_gather_notification(self, team, player):
        return Notification.objects.create(identifier='player-gather', team=team, player=player)

    def create_prevent_notification(self, team, player):
        return Notification.objects.create(identifier='player-prevent', team=team, player=player)

    # Pump notifications
    def create_retrieved_success_notification(self, team, player, resources, points):
        return Notification.objects.create(identifier='player-retrieved-success', team=team, player=player, resources_retrieved=resources, points_scored=points)

    def create_retrieved_failure_notification(self, team, player):
        return Notification.objects.create(identifier='player-retrieved-failure', team=team, player=player)


class Notification(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    identifier = models.CharField(max_length=255)

    # Set when this is a real player initiated action (mostly where they spend action points)
    action = models.BooleanField(default=True)

    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')

    # Whether to send this notification by e-mail or not
    # TODO probably needs to differentiate about who to e-mail
    email = models.BooleanField(default=False)

    # Fields to store data so we can parametrize notifications
    resources_retrieved = models.IntegerField(default=0)
    points_scored = models.IntegerField(default=0)

    # Field to store the target player for frontline actions
    target = models.ForeignKey('Player', related_name='+', null=True, blank=True)

    objects = NotificationManager()

    def save(self, *args, **kwargs):
        # Do e-mail sending here only if this is a new object
        if self.pk is None:
            self.send_email()

        super(Notification, self).save(*args, **kwargs)

    def send_email(self):
        if self.email and self.player.receive_email:
            subject = self.get_subject()
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = self.player.user.email

            content = self.get_message() + '<br><br>' + self.get_email_footer()

            try:
                msg = EmailMessage(subject, content, from_email, [to_email])
                msg.content_subtype = 'html'
                msg.send()
                logger.info('Sent e-mail to %s', to_email)
            except:
                logger.error('Could not send e-mail to %s', to_email)

    def get_email_footer(self):
        if not self.player.emails_unsubscribe_hash:
            self.player.update_unsubscribe_hash()
            self.player.save()

        return '''<a href="http://playrippleeffect.com%s">Unsubscribe</a>.''' % reverse('player_unsubscribe', args=(self.player.emails_unsubscribe_hash,))

    def get_message(self):
        """Messages are not stored in the database for parametrizability and translatability."""
        if self.identifier == 'player-inspected-safety':
            return 'inspected safety'
        elif self.identifier == 'player-inspected-production':
            return 'inspected production quality'
        elif self.identifier == 'player-improved-safety':
            return 'improved safety'
        elif self.identifier == 'player-improved-production':
            return 'improved production quality'
        elif self.identifier == 'player-received-poorvision-event':
            return 'received the Poor Vision event, affecting the whole team'
        elif self.identifier == 'player-received-tornado-event':
            return 'received the Tornado event, affecting the whole team'
        elif self.identifier == 'player-received-highmarket-event':
            return 'received the High Market event, affecting the whole team'
        elif self.identifier == 'player-received-increasedrisk-event':
            return 'received the Increased Risk event'
        elif self.identifier == 'player-received-lightning-event':
            return 'received the Lightning event'
        elif self.identifier == 'player-retrieved-success':
            return 'produced %d resources and scored %d points' % (self.resources_retrieved, self.points_scored)
        elif self.identifier == 'player-retrieved-failure':
            return 'tried to produce resources but triggered an incident'
        elif self.identifier == 'player-gather':
            return 'planned resource production'
        elif self.identifier == 'player-prevent':
            return 'placed a temporary barrier'
        elif self.identifier == 'frontline-safety':
            return "inspected %s's safety" % unicode(self.target)
        elif self.identifier == 'frontline-event':
            return "predicted %s's upcoming event" % unicode(self.target)

    def get_subject(self):
        # TODO modify subjects based on notification type
        if self.identifier == 'bla':
            return ''
        else:
            return 'New notification from Ripple Effect'

class Episode(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    first_day = models.ForeignKey('EpisodeDay', related_name='+', null=True)

    number = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.number)

class EpisodeDay(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    episode = models.ForeignKey(Episode)

    number = models.IntegerField(default=0)

    current = models.BooleanField(default=False)
    end = models.DateTimeField()

    next = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return str(self.number)

    def start(self):
        if self.episode.first_day == self:
            # We are at the start of an episode

            logger.info("Starting episode %s", str(self.episode))

            for team in Team.objects.all():
                team.start_episode(self.episode)

        for team in Team.objects.all():
            team.start_day(self)

        logger.info("Starting day %s", str(self))

    def secondsleft(self):
        if self.end < timezone.now():
            return 0
        else:
            diff = self.end - timezone.now()

            return diff.seconds + (diff.days * 24 * 60 * 60)


class TeamPlayer(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    role = models.CharField(max_length=255, default='office', choices=(('office', 'office'), ('frontline', 'frontline')))

    # 0 = no resource
    # 1 = resource
    gather_pile = models.CommaSeparatedIntegerField(max_length=255, default='', blank=True)
    gather_markers = models.IntegerField(default=0)

    # 0 = safety
    # 1 = incident
    risk_pile = models.CommaSeparatedIntegerField(max_length=255, default='', blank=True)
    prevent_markers = models.IntegerField(default=0)

    episode_events = models.CommaSeparatedIntegerField(max_length=255, default='', blank=True)

    active_events = models.CommaSeparatedIntegerField(max_length=255, blank=True, default='')

    lightning_hit = models.BooleanField(default=False)

    show_game_start = models.BooleanField(default=False)
    show_episode_start = models.BooleanField(default=False)
    show_turn_start = models.BooleanField(default=False)

    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')

    def __unicode__(self):
        return unicode(self.player)

    def startPiles(self):
        self.gather_pile = '0,1'
        self.risk_pile = '0,1'

    def addGatherCard(self, val):
        if val == 0 or val == 1:
            pile = self.gather_pile.split(',')
            pile.append(str(val))
            self.gather_pile = ','.join(pile)

    def addRiskCard(self, val):
        if val == 0 or val == 1:
            pile = self.risk_pile.split(',')
            pile.append(str(val))
            self.risk_pile = ','.join(pile)

    def inspect(self, p):
        if p == 'gather':
            pile = self.gather_pile
        elif p == 'risk':
            pile = self.risk_pile

        pile = pile.split(',')

        # Need to get half rounded up
        half = int(math.ceil(float(len(pile)) / 2.0))

        if self.team.is_event_active(Events.POOR_VISION):
            half -= 1

        result = pile[:half]

        random.shuffle(pile)

        save_value = ','.join(pile)

        if p == 'gather':
            self.gather_pile = save_value
        elif p == 'risk':
            self.risk_pile = save_value

        return result

    def invest(self, p):
        """Invests in target p pile."""

        if p == 'gather':
            add = '1'
        elif p == 'risk':
            add = '0'

        self.put_and_discard(add, p)

    def put_and_discard(self, value, target):
        """Puts a value in target pile, shuffles and discards a random value."""
        if target == 'gather':
            pile = self.gather_pile
        elif target == 'risk':
            pile = self.risk_pile

        pile = pile.split(',')
        pile.append(value)

        random.shuffle(pile)
        pile.pop(0)

        save_value = ','.join(pile)

        if target == 'gather':
            self.gather_pile = save_value
        elif target == 'risk':
            self.risk_pile = save_value

    def gather(self):
        self.gather_markers += 1

    def prevent(self):
        self.prevent_markers += 1

    def pump(self):
        # Steps to go through the gather pile
        gathersteps = self.gather_markers

        # Steps to go through the risk pile
        risksteps = self.gather_markers

        # Keep this for later reference
        planned_production = self.gather_markers

        pile = self.gather_pile.split(',')
        oil = 0 # Units of oil pumped
        reflow_production = [] # What we are going to put back in the deck
        result_production = [] # What we are going to return

        while True:
            result_step = []
            new_steps = 0

            for c in range(gathersteps):
                if pile:
                    output = pile.pop(0)

                    reflow_production.append(output)
                    result_step.append(output)

                    if output == '1':
                        oil += 1
                        new_steps += 1

            if result_step:
                result_production.append(result_step)

            if new_steps:
                gathersteps = new_steps
            else:
                break

        # We pump until everything is empty. Even if there are more markers than there are in the pile.
        self.gather_markers = 0

        self.gather_pile = ','.join(pile + reflow_production)
        # Shuffle happens later anyway with the decay step

        # Now do the same with the risk pile
        pile = self.risk_pile.split(',')
        risks = 0
        reflow_safety = []
        result_safety = []

        while True:
            result_step = []
            new_steps = 0

            for c in range(risksteps):
                if pile:
                    output = pile.pop(0)

                    reflow_safety.append(output)
                    result_step.append(output)

                    if output == '1':
                        risks += 1
                        new_steps += 1

            if result_step:
                result_safety.append(result_step)

            if new_steps:
                risksteps = new_steps
            else:
                break

        self.risk_pile = ','.join(pile + reflow_safety)

        # Both piles decay and are shuffled
        self.put_and_discard('0', 'gather')
        self.put_and_discard('1', 'risk')

        # If there are more risks than prevent markers, bad things will happen
        result = (oil, result_production, risks, result_safety, self.prevent_markers, planned_production)

        logger.info("Production result %s", str(result))

        self.prevent_markers = 0

        return result

    def get_event_for_day(self, day):
        if self.episode_events:
            return self.episode_events.split(',')[day.number-1]

    def add_active_event(self, event):
        new_events = self.active_events.split(',')
        new_events.append(event)

        self.active_events = ','.join(new_events)

    def clear_active_events(self):
        self.active_events = ''

    def is_event_active(self, event):
        return event in self.active_events.split(',')

    def get_active_events(self):
        return [el for el in self.active_events.split(',') if el]

    def hit_by_lightning(self):
        # TODO make function for taking the top card off a pile (drawing)
        effect = False

        pile = self.risk_pile.split(',')

        logger.info('Lightning risk pile: %s', str(pile))

        top_card = pile.pop(0)

        if top_card == '1':
            effect = True

            # The action drop is done outside of this method due to circumstances.

        pile = [top_card] + pile
        random.shuffle(pile)

        self.risk_pile = ','.join(pile)

        return effect


class Team(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, default='')

    # Open means a team can accept new players
    open = models.BooleanField(default=True)

    goal_zero_markers = models.IntegerField(default=0)
    goal_zero_streak = models.IntegerField(default=1)

    action_points = models.IntegerField(default=0)
    frontline_action_points = models.IntegerField(default=0)

    rank_points = models.IntegerField(default=0)
    victory_points = models.IntegerField(default=0)
    victory_points_episode = models.IntegerField(default=0)
    victory_points_turn = models.IntegerField(default=0)

    resources_collected = models.IntegerField(default=0)
    resources_collected_episode = models.IntegerField(default=0)

    leader = models.ForeignKey('Player', null=True, blank=True, related_name='ledteam')

    players = models.ManyToManyField('Player', through='TeamPlayer')

    active_events = models.CommaSeparatedIntegerField(max_length=255, blank=True, default='')

    def __unicode__(self):
        return self.name or self.pk

    def save(self, *args, **kwargs):
        super(Team, self).save(*args, **kwargs)

        self.update_rank()

    @models.permalink
    def get_absolute_url(self):
        return ('team_detail', [self.pk])

    def get_join_requests(self):
        return TeamJoinRequest.objects.filter(team=self, invite=False)

    def get_goal_zero_streak(self):
        return max(self.goal_zero_markers, self.goal_zero_streak)

    def start_episode(self, episode):
        # logger.info("Starting episode for team %s", str(self))

        if episode.number == 1:
            # Game start
            self.teamplayer_set.update(show_game_start=True)

        self.teamplayer_set.update(show_episode_start=True)
        
        playerCount = self.teamplayer_set.filter(role='office').count()

        # logger.info("Office player count: %d", playerCount)
        # logger.info("Gather: %s", self.teamplayer_set.filter(role='frontline')[0].gather_pile)

        # Stack both piles at the start of each episode
        # TODO already change the 0s and 1s here to strings
        gatherCards = (3*playerCount) * [0] + (3*playerCount) * [1]
        riskCards = (4*playerCount) * [0] + (2*playerCount) * [1]

        # Shuffle both piles
        random.shuffle(gatherCards)
        random.shuffle(riskCards)

        for tp in self.teamplayer_set.filter(role='office'):
            tp.startPiles()

            tp.gather_markers = 0
            tp.prevent_markers = 0

            # Add 6 gather cards
            # Add 6 risk cards
            for counter in range(6):
                tp.addGatherCard(gatherCards.pop())
                tp.addRiskCard(riskCards.pop())

            # logger.info("team player %s", str(tp))
            # logger.info("pile: %s", tp.gather_pile)

            tp.save()

        # For each TeamPlayer store the events they will be receiving this episode

        # Day lists start out empty
        day_lists = [[Events.NO_EVENT] * playerCount for counter in range(7)]

        def putEventInList(lists, day, event):
            for index in range(day, len(lists)):
                day_list = lists[index]

                if '0' in day_list:
                    # There is an empty spot in this day list
                    # Remove the empty spot and append the event
                    day_list.remove('0')
                    day_list.append(event)

                    # If we don't find a 0 in the day list, this will automatically go to the next one
                    break


        if episode.number == 1:
            for counter in range(playerCount):
                putEventInList(day_lists, random.randint(2, 6), Events.INCREASED_RISK)

            putEventInList(day_lists, random.randint(3, 6), Events.POOR_VISION)

        elif episode.number == 2:
            # First one high market event on day 2
            day_lists[1][0] = Events.HIGH_MARKET # It doesn't matter where we put this

            # Then increased risk events distributed in days 4,5,6
            for counter in range(playerCount):
                putEventInList(day_lists, random.randint(3, 5), Events.INCREASED_RISK)

            # Then one tornado event distributed in days 4,5,6
            putEventInList(day_lists, random.randint(3, 5), Events.TORNADO)

            # Then lightning events distributed in potentially days 3,4,5,6
            for counter in range(playerCount):
                putEventInList(day_lists, random.randint(2, 5), Events.LIGHTNING)

            # Then one poor vision event distributed potentially over in days 2,3,4,5,6,7
            putEventInList(day_lists, random.randint(1, 6), Events.POOR_VISION)

        # Randomize the lists per day
        [random.shuffle(day_list) for day_list in day_lists]

        index = 0
        for tp in self.teamplayer_set.filter(role='office'):
            # Stringify and slice them for each player
            player_events = [eventStack[index] for eventStack in day_lists]

            tp.episode_events = ','.join(player_events)
            tp.save()

            index += 1

        # Do these updates in the end to prevent them from being overwritten
        # Set action points to zero (these will be replenished on day start)
        Team.objects.filter(pk=self.pk).update(action_points=0)
        Team.objects.filter(pk=self.pk).update(frontline_action_points=0)

        # Set the per episode scores to 0 again
        Team.objects.filter(pk=self.pk).update(resources_collected_episode=0)
        Team.objects.filter(pk=self.pk).update(victory_points_episode=0)


    def start_day(self, day):
        # Draw event cards which can be either active for the player or for the team

        # Reset lightning hit at the start of every day
        self.teamplayer_set.update(lightning_hit=False)

        # Active events for teams are cleared at the start of a day
        self.clear_active_events()

        lightning_hits = 0

        for tp in self.teamplayer_set.filter(role='office'):
            # Active events for all players are cleared at the start of a day
            tp.clear_active_events()

            event = tp.get_event_for_day(day)

            if event == Events.HIGH_MARKET:
                self.add_active_event(Events.HIGH_MARKET)

                Notification.objects.create_received_highmarket_event_notification(self, tp.player)
            elif event == Events.INCREASED_RISK:
                tp.add_active_event(Events.INCREASED_RISK)

                tp.put_and_discard('1', 'risk')

                Notification.objects.create_received_increasedrisk_event_notification(self, tp.player)
            elif event == Events.TORNADO:
                self.add_active_event(Events.TORNADO)

                Notification.objects.create_received_tornado_event_notification(self, tp.player)
            elif event == Events.LIGHTNING:
                tp.add_active_event(Events.LIGHTNING)

                lightning_hit = tp.hit_by_lightning()

                if lightning_hit:
                    # TODO probably should move this inside the function
                    tp.lightning_hit = True
                    lightning_hits += 1

                # TODO make notification parametric based on effect

                Notification.objects.create_received_lightning_event_notification(self, tp.player)
            elif event == Events.POOR_VISION:
                self.add_active_event(Events.POOR_VISION)

                Notification.objects.create_received_poorvision_event_notification(self, tp.player)

            tp.save()
        self.save()

        # Put these after the save to prevent the stale model to overwrite the new values
        playerCount = self.teamplayer_set.filter(role='office').count()

        new_actions = 4 * playerCount

        logger.info("Player count %d, lightning hits %d, uncorrected new actions %d", playerCount, lightning_hits, new_actions)
        
        if lightning_hits > 0:
            new_actions -= (4 * lightning_hits)

        Team.objects.filter(pk=self.pk).update(action_points=new_actions)
        Team.objects.filter(pk=self.pk).update(frontline_action_points=2*playerCount)

        # Reset the per turn victory points counter
        Team.objects.filter(pk=self.pk).update(victory_points_turn=0)

        Team.objects.filter(pk=self.pk).update(goal_zero_markers=F('goal_zero_markers')+1)

        # At the start of a day reset all the markers for a team
        TeamPlayer.objects.filter(team=self).update(gather_markers=0)
        TeamPlayer.objects.filter(team=self).update(prevent_markers=0)

        # Show the turn start message
        TeamPlayer.objects.filter(team=self).update(show_turn_start=True)

    def add_active_event(self, event):
        new_events = self.active_events.split(',')
        new_events.append(event)

        self.active_events = ','.join(new_events)

    def clear_active_events(self):
        self.active_events = ''

    def is_event_active(self, event):
        return event in self.active_events.split(',')

    def get_active_events(self):
        return [el for el in self.active_events.split(',') if el]

    def get_office_players(self):
        return self.teamplayer_set.filter(role='office')

    def get_frontline_players(self):
        return self.teamplayer_set.filter(role='frontline')

    def update_rank(self):
        from redis_cache import get_redis_connection

        con = get_redis_connection('default')
        con.zadd('teamrank', self.pk, self.rank_points)

    def get_rank(self):
        from redis_cache import get_redis_connection

        con = get_redis_connection('default')
        return con.zrevrank('teamrank', self.pk)+1


class Player(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, default='')

    receive_email = models.BooleanField(default=True)
    emails_unsubscribe_hash = models.CharField(max_length=255, blank=True)

    user = models.OneToOneField(EmailUser)

    @models.permalink
    def get_absolute_url(self):
        return ('player_profile', [self.pk])

    def update_unsubscribe_hash(self):
        import uuid
        self.emails_unsubscribe_hash = uuid.uuid4().hex

    def __unicode__(self):
        return self.name or self.email()

    def get_led_team(self):
        try:
            return Team.objects.get(leader=self)
        except Team.DoesNotExist:
            return None

    def email(self):
        return self.user.email

    def get_intercom_hash(self):
        mac = hmac.new('pwGPevZCKMZEXZzhBwtOyWUlmPWCEBqe_R8dI6Xq', self.email(), hashlib.sha256)

        return mac.hexdigest()

    def get_teamplayer(self):
        return TeamPlayer.objects.get(player=self)


class TeamJoinRequest(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)

    # If this is true, it is an invitation, otherwise a player has requested to join themselves
    invite = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Request from %s to %s' % (unicode(self.player), self.team)


class GameManager(models.Manager):
    def get_latest_game(self):
        # This is the active game
        # TODO cache this call
        games = Game.objects.all().order_by('-start')

        if games:
            return games[0]
        else:
            # Creates an invalid game.
            return Game.objects.create(start=timezone.now(), end=timezone.now())

# Maybe remove the game class altogether TODO
class Game(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    objects = GameManager()

    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return str(self.pk)

    def started(self):
        return timezone.now() > self.start

    def over(self):
        return timezone.now() > self.end

    def active(self):
        return self.started() and not self.over()

    def initialize(self, start=None, episodeCount=2, dayLengthInMinutes=10):
        Episode.objects.all().delete()
        EpisodeDay.objects.all().delete()
        Notification.objects.all().delete()

        weekLength = 7

        if not start:
            start = timezone.now()

        self.start = start

        episodes = [Episode.objects.create(number=epCounter+1) for epCounter in range(episodeCount)]

        counter = 0

        previousDay = None

        for episode in episodes:
            first_day = True

            for dayCounter in range(weekLength):
                day = EpisodeDay.objects.create(episode=episode, number=(counter%7)+1, end=self.start+datetime.timedelta(minutes=dayLengthInMinutes*(counter+1)))

                if previousDay:
                    previousDay.next = day
                    previousDay.save()

                previousDay = day

                if first_day:
                    episode.first_day = day
                    episode.save()

                    first_day = False

                counter += 1

        self.end = previousDay.end # Previous day when we come out of the loop is the last day
        self.save()

        # Clear the ranking table
        from redis_cache import get_redis_connection

        con = get_redis_connection('default')
        con.delete('teamrank')
