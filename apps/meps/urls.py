from django.conf.urls.defaults import patterns, url

from meps import views


urlpatterns = patterns('', 
    url(r'^names/$', views.index_names, name='index_names'),
    url(r'^countries/$', views.index_countries, name='index_countries'),
    url(r'^country/(?P<country_code>[a-zA-Z][a-zA-Z])/$', views.index_by_country, name='index_by_country'),
    url(r'^groups/$', views.index_groups, name='index_groups'),
    url(r'^group/(?P<group>[a-zA-Z/-]+)/$', views.index_by_group, name='index_by_group'),

    url(r'^mep/(?P<mep_id>\w+)/$', views.mep, name='mep'),
    url(r'^mep/(?P<mep_id>\w+)/raw/$', views.mep_raw, name='mep_raw'),
    url(r'^mep/(?P<mep_id>\w+)/json/$', views.mep_json, name='mep_json'),
    url(r'^mep/(?P<mep_id>\w+)/addposition/$', views.mep_addposition, name='mep_addposition'),

    url(r'^moderation/$', views.moderation, name='moderation'),
    url(r'^moderation/get_unmoderated_positions$', views.moderation_get_unmoderated_positions, name='moderation_get_unmoderated_positions'),
    url(r'^moderation/moderate_position$', views.moderation_moderate_positions, name='moderation_moderate_positions'),
)

