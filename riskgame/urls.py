from django.conf.urls import patterns, url

from riskgame.views import TeamDetail
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'riskgame.views.index', name='index'),

    url(r'^pre/launch/$', 'riskgame.views.pre_launch', name='pre_launch'),

    url(r'^team/(?P<pk>\d+)/$', TeamDetail.as_view(), name='team_detail'),
    url(r'^team/create/$', 'riskgame.views.team_create', name='team_create'),
    url(r'^team/(?P<pk>\d+)/join/request/$', 'riskgame.views.request_team_join', name='request_team_join'),
    url(r'^dummy/$', TemplateView.as_view(template_name='riskgame/dummy.html'), name='dummy'),

    url(r'^players/$', 'riskgame.views.players', name='players'),
)
