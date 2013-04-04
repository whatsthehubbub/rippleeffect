from django.db import models
from django.db.models import F

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail

from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import random
import datetime

import logging
logger = logging.getLogger('ripple')



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
    def create_new_assignment_notification(self, team, player):
        return Notification.objects.create(identifier='player-new-assignment', team=team, player=player, message='', email=True)


class Notification(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    identifier = models.CharField(max_length=255)

    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')

    # Whether to send this notification by e-mail or not
    email = models.BooleanField(default=False)

    message = models.TextField()

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

            content = self.message + '<br><br>' + self.get_email_footer()

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

    def __unicode__(self):
        return str(self.id)

class EpisodeDay(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    episode = models.ForeignKey(Episode)

    current = models.BooleanField(default=False)
    end = models.DateTimeField()

    next = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return str(self.id)

    def start(self):
        if self.episode.first_day == self:
            # We are at the start of an episode

            logger.info("Starting episode %s", str(self.episode))

            for team in Team.objects.all():
                team.start_episode()

        for team in Team.objects.all():
            team.start_day()

        logger.info("Starting day %s", str(self))


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

    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')

    def __unicode__(self):
        return str(self.id)

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

        half = len(pile) / 2 + (len(pile) % 2 and 0 or 1)

        result = pile[:half]

        random.shuffle(pile)

        save_value = ','.join(pile)

        if p == 'gather':
            self.gather_pile = save_value
        elif p == 'risk':
            self.risk_pile = save_value

        return result

    def invest(self, p):
        # TODO can also add other values to piles for decay
        # refactor out adding type of card to certain pile
        if p == 'gather':
            pile = self.gather_pile
            add = '1'
        elif p == 'risk':
            pile = self.risk_pile
            add = '0'

        pile = pile.split(',')
        pile.append(add)

        random.shuffle(pile)
        pile.pop(0)

        save_value = ','.join(pile)

        if p == 'gather':
            self.gather_pile = save_value
        elif p == 'risk':
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

        pile = self.gather_pile.split(',')
        oil = 0 # Units of oil pumped

        while gathersteps > 0:
            if pile:
                output = pile.pop(0)

                if output == '1':
                    oil += 1
                    # Do an extra pump for every oil we pump
                    gathersteps += 1

            gathersteps -= 1

        self.gather_markers = 0

        self.gather_pile = ','.join(pile)

        # Now do the same with the risk pile

        pile = self.risk_pile.split(',')
        risks = 0

        while risksteps > 0:
            if pile:
                output = pile.pop(0)

                if output == '1':
                    risks += 1

                    # Do an extra risk resolve for every risk we get
                    risksteps += 1

            risksteps -= 1

        self.risk_pile = ','.join(pile)

        # If there are more risks than prevent markers, bad things will happen
        result = (oil, risks, self.prevent_markers)

        self.prevent_markers = max(0, self.prevent_markers - risks)

        return result

class Team(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, default='')

    # Open means a team can accept new players
    open = models.BooleanField(default=True)

    goal_zero_markers = models.IntegerField(default=0)
    action_points = models.IntegerField(default=0)

    score = models.IntegerField(default=0)

    leader = models.ForeignKey('Player', null=True, related_name='ledteam')

    players = models.ManyToManyField('Player', through='TeamPlayer')

    # TODO both these fields can probably be removed for a global timezoned game
    # Which day we are at currently and when to check again for a move
    currentDay = models.ForeignKey("EpisodeDay", null=True, blank=True)
    check_next = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name or self.id

    @models.permalink
    def get_absolute_url(self):
        return ('team_detail', [self.id])

    def get_join_requests(self):
        return TeamJoinRequest.objects.filter(team=self, invite=False)

    def start_episode(self):
        playerCount = self.players.count()

        gatherCards = (3*playerCount) * [0] + (3*playerCount) * [1]
        riskCards = (4*playerCount) * [0] + (2*playerCount) * [1]

        # Shuffle both piles
        random.shuffle(gatherCards)
        random.shuffle(riskCards)

        for tp in self.teamplayer_set.all():
            tp.startPiles()

            tp.gather_markers = 0
            tp.prevent_markers = 0

            # Add 6 gather cards
            # Add 6 risk cards
            for counter in range(6):
                tp.addGatherCard(gatherCards.pop())
                tp.addRiskCard(riskCards.pop())

            tp.save()

        Team.objects.filter(id=self.id).update(action_points=0)

    def start_day(self):
        playerCount = self.players.count()

        Team.objects.filter(id=self.id).update(action_points=4*playerCount)
        Team.objects.filter(id=self.id).update(goal_zero_markers=F('goal_zero_markers')+1)

    # def update_current_day(self):
    #     team_local_now = datetime.datetime.now(self.leader.timezone)
    #     naive_team_local_now = team_local_now.replace(tzinfo=None)

    #     print 'ntln', naive_team_local_now

    #     if self.currentDay:
    #         naive_day_end = self.currentDay.end.replace(tzinfo=None)

    #         print 'nde', naive_day_end

    #         if naive_team_local_now >= naive_day_end:
    #             self.currentDay = self.currentDay.next
    #     else:
    #         game = Game.objects.get_latest_game()
    #         naive_game_start = game.start.replace(tzinfo=None)

    #         print 'ngs', naive_game_start

    #         if naive_team_local_now > naive_game_start:
    #             # Set to the first day
    #             # TODO check for game over, game pre-start
    #             days = EpisodeDay.objects.all().order_by('end')
    #             self.currentDay = days[0]

    #     # Else we stay on the current day and update our check_next value
    #     # TODO increase the check next value
    #     self.check_next = timezone.now() + datetime.timedelta(minutes=1)
    #     self.save()


class Player(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, default='')
    onelinebio = models.CharField(max_length=140, default='', blank=True)

    receive_email = models.BooleanField(default=True)
    emails_unsubscribe_hash = models.CharField(max_length=255, blank=True)

    user = models.OneToOneField(EmailUser)

    def update_unsubscribe_hash(self):
        import uuid
        self.emails_unsubscribe_hash = uuid.uuid4().hex

    def __unicode__(self):
        return str(self.user)

    def get_led_team(self):
        try:
            return Team.objects.get(leader=self)
        except Team.DoesNotExist:
            return None

    def email(self):
        return self.user.email

class TeamJoinRequest(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)

    # If this is true, it is an invitation, otherwise a player has requested to join themselves
    invite = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Request from %s to %s' % (str(self.player), self.team)


class GameManager(models.Manager):
    def get_latest_game(self):
        # This is the active game
        # TODO cache this call
        games = Game.objects.all().order_by('-start')

        if games:
            return games[0]
        else:
            return Game.objects.create(start=timezone.now())

# Maybe remove the game class altogether TODO
class Game(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    objects = GameManager()

    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return str(self.id)

    def started(self):
        return timezone.now() > self.start

    def over(self):
        return timezone.now() > self.end

    def active(self):
        return self.started() and not self.over()

    def initialize(self, start=None, episodeCount=2, weekLength=7, dayLengthInMinutes=10):

        if not start:
            start = timezone.now()

        self.start = start


        Team.objects.all().update(currentDay=None)
        Team.objects.all().update(check_next=None)

        Episode.objects.all().delete()
        EpisodeDay.objects.all().delete()

        episodes = [Episode.objects.create() for epCounter in range(episodeCount)]

        counter = 1

        previousDay = None

        for episode in episodes:
            first_day = True

            for dayCounter in range(weekLength):
                day = EpisodeDay.objects.create(episode=episode, end=self.start+datetime.timedelta(minutes=dayLengthInMinutes*counter))

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
