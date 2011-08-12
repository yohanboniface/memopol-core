from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('trends.views',
    url(r'^mep/(?P<mep_id>\w+)-comparaison.png$', 'comparaison_trends_for_mep', name='comparaison_trends'),
    url(r'^mep/(?P<mep_id>\w+)-bar.png$', 'bar_trends_for_mep', name='bar_trends'),
    url(r'^mep/(?P<mep_id>\w+).png$', 'trends_for_mep', name='trends'),
    url(r'^recommendation/(?P<recommendation_id>[0-9]+)-group.png$', 'recommendation_group', name='recommendation_group'),
)
