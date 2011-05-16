from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail

from votes.models import Proposal

urlpatterns = patterns('',
    url(r'^$', list_detail.object_list, {'queryset': Proposal.objects.all()}, name='index'),
    url(r'^(?P<object_id>[a-zA-Z/-_]+)/$', list_detail.object_detail, {'queryset': Proposal.objects.all(), 'template_object_name': 'vote'}, name='detail'),
)
