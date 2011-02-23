import os

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.static import serve

from memopol2.main import views

admin.autodiscover()

urlpatterns = patterns('', # pylint: disable=C0103
    url(r'^$', views.index_countries, name='index'),

    url(r'^names/$', views.index_names, name='index_names'),
    url(r'^countries/$', views.index_countries, name='index_countries'),
    url(r'^country/(?P<country_code>[a-zA-Z][a-zA-Z])/$', views.index_by_country, name='index_by_country'),
    url(r'^groups/$', views.index_groups, name='index_groups'),
    url(r'^group/(?P<group>[a-zA-Z/-]+)/$', views.index_by_group, name='index_by_group'),


    url(r'^mep/(?P<mep_id>\w+)/$', views.mep, name='mep'),
    url(r'^mep/(?P<mep_id>\w+)/raw/$', views.mep_raw, name='mep_raw'),
    url(r'^mep/(?P<mep_id>\w+)/addposition/$', views.mep_addposition, name='mep_addposition'),


    url(r'^moderation/$', views.moderation, name='moderation'),
    url(r'^moderation/get_unmoderated_positions$', views.moderation_get_unmoderated_positions, name='moderation_get_unmoderated_positions'),
    url(r'^moderation/moderate_position$', views.moderation_moderate_positions, name='moderation_moderate_positions'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

# hack to autodiscover static files location in dev mode
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(.*)$', serve, {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
    )
# TODO: static files location in production
# should never be served by django, settings.MEDIA_URL is the right way to do
