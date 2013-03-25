from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'riskgame.views.index', name='index'),

    url(r'^pre/launch/$', 'riskgame.views.pre_launch', name='pre_launch'),
)
