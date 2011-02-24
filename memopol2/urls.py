import os

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.static import serve

from django.conf.urls.defaults import *

from meps import views

admin.autodiscover()

urlpatterns = patterns('', # pylint: disable=C0103
    url(r'^$', views.index_countries, name='index'),
    url(r'^meps/', include('meps.urls', namespace='meps', app_name='meps')),
    url(r'^mps/', include('mps.urls', namespace='mps', app_name='mps')),
    url(r'^votes/', include('votes.urls', namespace='votes', app_name='votes')),
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
