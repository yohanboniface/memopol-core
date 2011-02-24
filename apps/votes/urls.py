from django.conf.urls.defaults import patterns, url

from votes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<vote_name>[a-zA-Z/-_]+)/$', views.detail, name='detail'),
)
