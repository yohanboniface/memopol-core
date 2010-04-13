from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^memopol2/', include('memopol2.foo.urls')),

    (r'^$', 'memopol2.main.views.index'),


    (r'^mep/$', 'memopol2.main.views.index'),
    (r'^mep/(?P<mep_id>[a-zA-Z0-9]+)/$', 'memopol2.main.views.mep'),
    (r'^mep/(?P<mep_id>[a-zA-Z0-9]+)/raw/$', 'memopol2.main.views.raw'),
    (r'^mep/(?P<mep_id>[a-zA-Z0-9]+)/addposition/$', 'memopol2.main.views.addposition'),


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
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, '..', 'static')}),
    )
