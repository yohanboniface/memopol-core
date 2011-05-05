from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail

from votes import views
from votes.models import Vote

urlpatterns = patterns('',
    url(r'^$', list_detail.object_list, {'queryset': Vote.objects.all()}, name='index'),
    url(r'^(?P<vote_name>[a-zA-Z/-_]+)/$', views.detail, name='detail'),
)
