from django.conf.urls import patterns, url

from riskgame.views import TeamDetail
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'riskgame.views.index', name='index'),

    # url(r'^pre/launch/$', 'riskgame.views.pre_launch', name='pre_launch'),

    url(r'^team/$', 'riskgame.views.team', name='team'),
    url(r'^team/(?P<pk>\d+)/$', TeamDetail.as_view(), name='team_detail'),
    url(r'^team/create/$', 'riskgame.views.team_create', name='team_create'),
    url(r'^team/(?P<pk>\d+)/join/request/$', 'riskgame.views.request_team_join', name='request_team_join'),
    url(r'^team/(?P<pk>\d+)/join/accept/$', 'riskgame.views.accept_team_join', name='accept_team_join'),

    url(r'^dummy/$', TemplateView.as_view(template_name='riskgame/dummy.html'), name='dummy'),

    url(r'^players/$', 'riskgame.views.players', name='players'),

    url(r'^players/(\S+?)/unsubscribe/$', 'riskgame.views.player_unsubscribe', name='player_unsubscribe'),

    url(r'^home/$', 'riskgame.views.home', name='home'),

    url(r'^game/start/$', 'riskgame.views.game_start', name='game_start'),

    url(r'^play/inspect/$', 'riskgame.views.play_inspect', name='play_inspect'),
    url(r'^play/invest/$', 'riskgame.views.play_invest', name='play_invest'),
    url(r'^play/gather/$', 'riskgame.views.play_gather', name='play_gather'),
    url(r'^play/prevent/$', 'riskgame.views.play_prevent', name='play_prevent'),
    url(r'^play/pump/$', 'riskgame.views.play_pump', name='play_pump'),
)
