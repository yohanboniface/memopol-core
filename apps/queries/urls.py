from django.conf.urls.defaults import patterns, url

from meps import views


urlpatterns = patterns('', 
    url(r'^$', views.query, name='query'),
)

