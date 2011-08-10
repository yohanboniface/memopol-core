from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail, ListView
from memopol2 import utils

from meps.models import MEP, Country, Group, Committee, Delegation, Organization, Building
from reps.models import Party

from views import BuildingDetailView, MEPView

country_dict = {
  'queryset': Country.objects.all(),
  'slug_field': 'code',
  'template_name': 'meps/container_detail.html',
  'extra_context': {
    'hidden_fields': ['country'],
    'header_template': 'meps/country_header.html',
  },
}
party_dict = {
  'queryset': Party.objects.all(),
  'template_name': 'meps/container_detail.html',
  'extra_context': {
    'hidden_fields': ['party'],
    'header_template': 'meps/named_header.html',
  },
}
group_dict = {
  'queryset': Group.objects.all(),
  'slug_field': 'abbreviation',
  'template_name': 'meps/container_detail.html',
  'extra_context': {
    'hidden_fields': ['group'],
    'header_template': 'meps/group_header.html',
  },
}
delegation_dict = {
  'queryset': Delegation.objects.all(),
  'template_name': 'meps/container_detail.html',
  'extra_context': {
    'hidden_fields': [],
    'header_template': 'meps/named_header.html',
  },
}
committe_dict = {
  'queryset': Committee.objects.all(),
  'slug_field': 'abbreviation',
  'template_name': 'meps/container_detail.html',
  'extra_context': {
    'hidden_fields': [],
    'header_template': 'meps/named_header.html',
  },
}
organization_dict = {
  'queryset': Organization.objects.all(),
  'template_name': 'meps/container_detail.html',
  'extra_context': {
    'hidden_fields': [],
    'header_template': 'meps/named_header.html',
  },
}

urlpatterns = patterns('meps.views',
    # those view are *very* expansive. we cache them in RAM for a week
    url(r'^names/$', utils.cached(3600*24*7)(list_detail.object_list), {'queryset': MEP.objects.filter(active=True)}, name='index_names'),
    url(r'^inactive/$', utils.cached(3600*24*7)(list_detail.object_list), {'queryset': MEP.objects.filter(active=False)}, name='index_inactive'),
    url(r'^score/$', list_detail.object_list, {'queryset': MEP.objects.filter(active=True).order_by('-total_score'), 'extra_context' : {'score_listing' : True}}, name='scores'),

    url(r'^organization/$', ListView.as_view(model=Organization), name='index_organizations'),
    url(r'^organization/(?P<object_id>[0-9]+)/$', list_detail.object_detail, organization_dict, name='index_by_organization'),
    url(r'^country/$', ListView.as_view(model=Country), name='index_countries'),
    url(r'^country/(?P<slug>[a-zA-Z][a-zA-Z])/$', list_detail.object_detail, country_dict, name='index_by_country'),
    url(r'^group/$', ListView.as_view(model=Group), name='index_groups'),
    url(r'^group/(?P<slug>[a-zA-Z/-]+)/$', list_detail.object_detail, group_dict,  name='index_by_group'),
    url(r'^committee/$', ListView.as_view(model=Committee), name='index_committees'),
    url(r'^committee/(?P<slug>[A-Z]+)/$', list_detail.object_detail, committe_dict, name='index_by_committee'),
    url(r'^delegation/$', ListView.as_view(model=Delegation), name='index_delegations'),
    url(r'^delegation/(?P<object_id>[0-9]+)/$', list_detail.object_detail, delegation_dict, name='index_by_delegation'),
    url(r'^party/$', ListView.as_view(model=Party), name='index_parties'),
    url(r'^party/(?P<object_id>[0-9]+)/$', list_detail.object_detail, party_dict,  name='index_by_party'),
    url(r'^floor/$', list_detail.object_list, {'queryset': Building.objects.all().order_by('postcode')}, name='index_floor'),
    url(r'^floor/brussels/(?P<pk>\w+)/(?P<floor>\w+)/$', BuildingDetailView.as_view(), name='bxl_floor'),

    url(r'^deputy/(?P<pk>\w+)/$', MEPView.as_view(), name='mep'),
    url(r'^deputy/(?P<pk>\w+)/dataporn/$', MEPView.as_view(template_name="meps/dataporn.html"), name='mep_dataporn'),
    url(r'^deputy/(?P<pk>\w+)/contact$', MEPView.as_view(template_name="meps/mep_contact.html"), name='mep_contact'),
)

urlpatterns += patterns('meps.views',
    url(r'^mep/(?P<ep_id>[0-9]+)/picture.jpg$', 'get_mep_picture',
        name='mep-picture'),
)
