from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.core.mail import send_mail

class EmailUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=EmailUserManager.normalize_email(email)
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save()

        return user


class EmailUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='E-mail address', max_length=255, unique=True, db_index=True)

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


class Team(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, default='')

    # Open means a team can accept new players
    open = models.BooleanField(default=True)

    goal_zero_score = models.IntegerField(default=0)
    resource_score = models.IntegerField(default=0)
    victory_points = models.IntegerField(default=0)

    leader = models.ForeignKey('Player', null=True, related_name='ledteam')

    def __unicode__(self):
        return self.name or self.id

    @models.permalink
    def get_absolute_url(self):
        return ('team_detail', [self.id])

    def get_join_requests(self):
        return TeamJoinRequest.objects.filter(team=self, invite=False)

class Player(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, default='')
    onelinebio = models.CharField(max_length=140, default='')
    role = models.CharField(max_length=255, choices=(("OFFICE", "Office"), ("FRONTLINE", "Frontline")), default="OFFICE")

    receive_email = models.BooleanField(default=True)

    user = models.OneToOneField(EmailUser)

    team = models.ForeignKey(Team, null=True, blank=True)

    # TODO add team role

    def __unicode__(self):
        return str(self.user)

    def get_led_team(self):
        try:
            return Team.objects.get(leader=self)
        except Team.DoesNotExist:
            return None

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
        games = Game.objects.all().order_by('-datecreated')

        if games:
            return games[0]
        else:
            return Game.objects.create()

class Game(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    datestart = models.DateTimeField()

    objects = GameManager()

    def __unicode__(self):
        return str(self.id)

    def started(self):
        return timezone.now() > self.datestart
