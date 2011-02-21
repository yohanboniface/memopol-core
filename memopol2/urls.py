import os

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', # pylint: disable=C0103
    url(r'^$', 'memopol2.main.views.index_countries', name='index'),

    url(r'^names/$', 'memopol2.main.views.index_names', name='index_names'),
    url(r'^countries/$', 'memopol2.main.views.index_countries', name='index_countries'),
    url(r'^country/(?P<country_code>[a-zA-Z][a-zA-Z])/$', 'memopol2.main.views.index_by_country', name='index_by_country'),
    url(r'^groups/$', 'memopol2.main.views.index_groups', name='index_groups'),
    url(r'^group/(?P<group>[a-zA-Z/-]+)/$', 'memopol2.main.views.index_by_group', name='index_by_group'),


    url(r'^mep/(?P<mep_id>[a-zA-Z0-9]+)/$', 'memopol2.main.views.mep', name='mep'),
    url(r'^mep/(?P<mep_id>[a-zA-Z0-9]+)/raw/$', 'memopol2.main.views.mep_raw', name='mep_raw'),
    url(r'^mep/(?P<mep_id>[a-zA-Z0-9]+)/addposition/$', 'memopol2.main.views.mep_addposition', name='mep_addposition'),


    url(r'^moderation/$', 'memopol2.main.views.moderation', name='moderation'),
    url(r'^moderation/get_unmoderated_positions$', 'memopol2.main.views.moderation_get_unmoderated_positions', name='moderation_get_unmoderated_positions'),
    url(r'^moderation/moderate_position$', 'memopol2.main.views.moderation_moderate_positions', name='moderation_moderate_positions'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

# hack to autodiscover static files location in dev mode
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
    )
# TODO: static files location in production
# should never be served by django, settings.MEDIA_URL is the right way to do
