from django.conf.urls.defaults import patterns, url

from mps import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<mp_id>[a-zA-Z]+)/$', views.detail, name='detail'),
)
