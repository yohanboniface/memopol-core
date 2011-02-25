from django.conf.urls.defaults import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.query, name='query'),
    url(r'^bla$', views.bla, name='bla'),
)

