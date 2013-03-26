from django.conf.urls import patterns, url

from riskgame.views import TeamDetail

urlpatterns = patterns('',
    url(r'^$', 'riskgame.views.index', name='index'),

    url(r'^pre/launch/$', 'riskgame.views.pre_launch', name='pre_launch'),

    url(r'^team/(?P<pk>\d+)/$', TeamDetail.as_view(), name='team_detail'),
)
