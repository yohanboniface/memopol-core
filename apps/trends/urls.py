from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('trends.views',
    url(r'^mep/(?P<mep_id>\w+)-comparaison.png$', 'comparaison_trends_for_mep', name='comparaison_trends'),
    url(r'^mep/(?P<mep_id>\w+)-bar.png$', 'bar_trends_for_mep', name='bar_trends'),
    url(r'^mep/(?P<mep_id>\w+).png$', 'trends_for_mep', name='trends'),
    url(r'^proposal/(?P<proposal_id>\w+)-countries-map.svg$', 'proposal_countries_map', name='recommendation_countries_map'),
    url(r'^proposal/groups-(?P<proposal_id>\w+)-repartition.png$', 'group_proposal_score', name='group_proposal_score'),
    url(r'^proposal/groups-(?P<proposal_id>\w+)-repartition-stacked.png$', 'group_proposal_score_stacked', name='group_proposal_score_stacked'),
    url(r'^recommendation/(?P<recommendation_id>[0-9]+)-group.png$', 'recommendation_group', name='recommendation_group'),
    url(r'^recommendation/(?P<recommendation_id>[0-9]+)-countries.png$', 'recommendation_countries', name='recommendation_countries'),
    url(r'^recommendation/(?P<recommendation_id>[0-9]+)-countries-absolute.png$', 'recommendation_countries_absolute', name='recommendation_countries_absolute'),
)
