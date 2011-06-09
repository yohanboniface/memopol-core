from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('trends.views',
    url(r'^mep/(?P<mep_id>\w+).png$', 'trends_for_mep', name='trends'),
)
