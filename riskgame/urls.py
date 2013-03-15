from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'riskgame.views.index', name='index'),
)
