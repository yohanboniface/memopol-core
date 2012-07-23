from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from memopol2 import utils

from mps.models import MP, Group, Department
from mps.views import MPList, MPsFromModel, MPView
from reps.models import Opinion


urlpatterns = patterns('mps.views',
    # the /names view is *very* expansive. we cache it in RAM for a week
    url(r'^$', utils.cached(3600*24*7)(MPList.as_view()), name='index'),

    url(r'^depute/(?P<pk>[a-zA-Z]+)/$', MPView.as_view(), name='mp'),
    url(r'^depute/(?P<pk>[a-zA-Z]+)/contact$', DetailView.as_view(model=MP, context_object_name='mp', template_name='mps/mp_contact.html'), name='mp_contact'),
    url(r'^group/$', ListView.as_view(queryset=Group.with_mps_count()), name='index_groups'),
    url(r'^group/(?P<pk>.+)/$', MPsFromModel.as_view(model=Group, template_name='mps/container_detail.html'), name='index_by_group'),
    url(r'^department/$', ListView.as_view(queryset=Department.with_mps_count().order_by('number')), name='index_departments'),
    url(r'^department/(?P<pk>.+)/$', MPsFromModel.as_view(model=Department, template_name='mps/container_detail.html'), name='index_by_department'),
    url(r'^opinion/$', ListView.as_view(queryset=Opinion.with_mps_count().order_by('-_date').select_related('_author')), name='index_opinions'),
    url(r'^opinion/(?P<pk>[0-9]+)/$', DetailView.as_view(model=Opinion, template_name="mps/opinion_detail.html"), name='index_by_opinions'),

    url(r'^vote/', include("mps_votes.urls", namespace="votes", app_name="mps_urls")),

    url(r'^votes/$', lambda request: redirect(reverse("mps:votes:index_votes"))),

    url(r'^nosdeputes/(?P<pk>.+)/$', 'get_nosdeputes_widget')
)
