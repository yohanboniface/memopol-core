from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail

from mps import views
from mps.models import MP

urlpatterns = patterns('',
    url(r'^$', list_detail.object_list, {'queryset': MP.objects.filter(active=True)}, name='index'),
    url(r'^(?P<mp_id>[a-zA-Z]+)/$', views.detail, name='detail'),
)
