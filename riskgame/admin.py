from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from riskgame.models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = EmailUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EmailUser

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class EmailUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(EmailUser, EmailUserAdmin)



# class ValidEmailDomainAdmin(admin.ModelAdmin):
#     list_display = ('datecreated', 'name')
# admin.site.register(ValidEmailDomain, ValidEmailDomainAdmin)

class TeamPlayerAdmin(admin.ModelAdmin):
    list_display = ('role', 'team', 'player', 'gather_pile', 'risk_pile', 'episode_events', 'active_events')
admin.site.register(TeamPlayer, TeamPlayerAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'victory_points', 'rank_points', 'resources_collected', 'action_points', 'frontline_action_points', 'goal_zero_markers', 'goal_zero_streak', 'active_events', 'get_rank')
admin.site.register(Team, TeamAdmin)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email')
admin.site.register(Player, PlayerAdmin)

# class TeamJoinRequestAdmin(admin.ModelAdmin):
#     list_display = ('team', 'player')
# admin.site.register(TeamJoinRequest, TeamJoinRequestAdmin)

class GameAdmin(admin.ModelAdmin):
    list_display = ('datecreated', 'start', 'end', 'started', 'over', 'active')
admin.site.register(Game, GameAdmin)

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('datecreated', 'first_day', 'number')
admin.site.register(Episode, EpisodeAdmin)

class EpisodeDayAdmin(admin.ModelAdmin):
    list_display = ('datecreated', 'episode', 'number', 'current', 'end', 'next', 'secondsleft')
admin.site.register(EpisodeDay, EpisodeDayAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('datecreated', 'team', 'player', 'identifier', 'target')
admin.site.register(Notification, NotificationAdmin)
