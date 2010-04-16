from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^memopol2/', include('memopol2.foo.urls')),

    (r'^$', 'memopol2.main.views.index_countries'),

    (r'^names/$', 'memopol2.main.views.index_names'),
    (r'^countries/$', 'memopol2.main.views.index_countries'),
    (r'^country/(?P<country_code>[a-zA-Z][a-zA-Z])/$', 'memopol2.main.views.index_by_country'),
    (r'^groups/$', 'memopol2.main.views.index_groups'),
    (r'^group/(?P<group>[a-zA-Z/-]+)/$', 'memopol2.main.views.index_by_group'),


    (r'^mep/(?P<mep_id>[a-zA-Z0-9]+)/$', 'memopol2.main.views.mep'),
    (r'^mep/(?P<mep_id>[a-zA-Z0-9]+)/raw/$', 'memopol2.main.views.mep_raw'),
    (r'^mep/(?P<mep_id>[a-zA-Z0-9]+)/addposition/$', 'memopol2.main.views.mep_addposition'),


    (r'^moderation/$', 'memopol2.main.views.moderation'),
    (r'^moderation/get_unmoderated_positions$', 'memopol2.main.views.moderation_get_unmoderated_positions'),
    (r'^moderation/moderate_position$', 'memopol2.main.views.moderation_moderate_positions'),

    #(r'^comments/', include('django.contrib.comments.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # static files for development    , {'document_root': '/path/to/media'}),

)

import settings, os
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
    )
