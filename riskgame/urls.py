from django.conf.urls import patterns, url

from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'riskgame.views.index', name='index'),

    # url(r'^pre/launch/$', 'riskgame.views.pre_launch', name='pre_launch'),

    url(r'^teams/$', 'riskgame.views.teams', name='teams'),
    url(r'^teams/(?P<pk>\d+)/$', 'riskgame.views.team_detail', name='team_detail'),
    url(r'^teams/your/$', 'riskgame.views.team_your', name="team_your"),
    # url(r'^teams/create/$', 'riskgame.views.team_create', name='team_create'),
    # url(r'^team/(?P<pk>\d+)/join/request/$', 'riskgame.views.request_team_join', name='request_team_join'),
    # url(r'^team/(?P<pk>\d+)/join/accept/$', 'riskgame.views.accept_team_join', name='accept_team_join'),

    url(r'^dummy/$', TemplateView.as_view(template_name='riskgame/dummy.html'), name='dummy'),

    url(r'^players/$', 'riskgame.views.players', name='players'),

    url(r'^notifications/$', 'riskgame.views.notifications', name='notifications'),

    url(r'^players/(?P<pk>\d+)/$', 'riskgame.views.player_profile', name='player_profile'),
    url(r'^players/you/$', 'riskgame.views.player_profile_own', name='player_profile_own'),
    url(r'^players/you/edit/$', 'riskgame.views.player_profile_edit', name='player_profile_edit'),

    url(r'^players/(\S+?)/unsubscribe/$', 'riskgame.views.player_unsubscribe', name='player_unsubscribe'),

    url(r'^home/$', 'riskgame.views.home', name='home'),

    url(r'^game/start/$', 'riskgame.views.game_start', name='game_start'),

    url(r'^play/inspect/$', 'riskgame.views.play_inspect', name='play_inspect'),
    url(r'^play/improve/$', 'riskgame.views.play_invest', name='play_invest'),
    url(r'^play/plan/$', 'riskgame.views.play_gather', name='play_gather'),
    url(r'^play/barrier/$', 'riskgame.views.play_prevent', name='play_prevent'),
    url(r'^play/confirm-production/$', 'riskgame.views.play_confirm_pump', name='play_confirm_pump'),
    url(r'^play/produce/$', 'riskgame.views.play_pump', name='play_pump'),

    url(r'^frontline/safety/$', 'riskgame.views.inspect_risks', name='frontline_risks'),
    url(r'^frontline/event/$', 'riskgame.views.inspect_event', name='frontline_event'),
)
