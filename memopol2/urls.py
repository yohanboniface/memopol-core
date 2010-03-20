from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^memopol2/', include('memopol2.foo.urls')),
    
    (r'^mep/$', 'memopol2.show.views.index'),
    (r'^mep/(?P<mep_id>[a-fA-F0-9]+)/$', 'memopol2.show.views.mep'),
    (r'^mep/(?P<mep_id>[a-fA-F0-9]+)/addposition/$', 'memopol2.show.views.addposition'),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
