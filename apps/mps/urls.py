from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from memopol2 import utils

from mps.models import MP, Group, Department
from votes.models import Proposal
from reps.models import Opinion

urlpatterns = patterns('',
    # the /names view is *very* expansive. we cache it in RAM for a week
    url(r'^$', utils.cached(3600*24*7)(ListView.as_view(queryset=MP.objects.filter(active=True))), name='index'),

    url(r'^depute/(?P<pk>[a-zA-Z]+)/$', DetailView.as_view(model=MP, context_object_name='mp'), name='mp'),
    url(r'^depute/(?P<pk>[a-zA-Z]+)/contact$', DetailView.as_view(model=MP, context_object_name='mp', template_name='mps/mp_contact.html'), name='mp_contact'),
    url(r'^group/$', ListView.as_view(model=Group), name='index_groups'),
    url(r'^group/(?P<pk>.+)/$', DetailView.as_view(model=Group, template_name='mps/container_detail.html'), name='index_by_group'),
    url(r'^department/$', ListView.as_view(queryset=Department.objects.order_by('number')), name='index_departments'),
    url(r'^department/(?P<pk>.+)/$', DetailView.as_view(model=Department, template_name='mps/container_detail.html'), name='index_by_department'),
    url(r'^opinion/$', ListView.as_view(queryset=Opinion.objects.filter(institution="FR")), name='index_opinions'),

    url(r'^votes/$', ListView.as_view(queryset=Proposal.objects.filter(institution="FR")), name='index_votes'),
)
