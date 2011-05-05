from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail

from mps.models import MP

urlpatterns = patterns('',
    url(r'^$', list_detail.object_list, {'queryset': MP.objects.filter(active=True)}, name='index'),
    url(r'^mp/(?P<object_id>[a-zA-Z]+)/$', list_detail.object_detail, {'queryset': MP.objects.all(), 'template_object_name': 'mp'}, name='detail'),
)
