from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail
from memopol2 import utils

from meps.models import MEP, Country, Group, Committee, Delegation, Organization, Building
from reps.models import Party

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
mep_dict = {'queryset': MEP.objects.all(), 'slug_field': 'id', 'template_object_name': 'mep'}
mep_dict_dataporn = {'queryset': MEP.objects.all(), 'slug_field': 'id', 'template_object_name': 'mep', 'template_name': 'meps/dataporn.html'}
mep_contact_dict = {'queryset': MEP.objects.all(), 'slug_field': 'id',
                    'template_name': 'meps/mep_contact.html',
                    'template_object_name': 'mep'}

urlpatterns = patterns('meps.views',
    # those view are *very* expansive. we cache them in RAM for a week
    url(r'^names/$', utils.cached(3600*24*7)(list_detail.object_list), {'queryset': MEP.objects.filter(active=True)}, name='index_names'),
    url(r'^inactive/$', utils.cached(3600*24*7)(list_detail.object_list), {'queryset': MEP.objects.filter(active=False)}, name='index_inactive'),
    url(r'^score/$', list_detail.object_list, {'queryset': MEP.objects.filter(active=True).order_by('-total_score'), 'extra_context' : {'score_listing' : True}}, name='scores'),

    url(r'^organization/$', list_detail.object_list, {'queryset': Organization.objects.all()}, name='index_organizations'),
    url(r'^organization/(?P<object_id>[0-9]+)/$', list_detail.object_detail, organization_dict, name='index_by_organization'),
    url(r'^country/$', list_detail.object_list, {'queryset': Country.objects.with_counts()}, name='index_countries'),
    url(r'^country/(?P<slug>[a-zA-Z][a-zA-Z])/$', list_detail.object_detail, country_dict, name='index_by_country'),
    url(r'^group/$', list_detail.object_list, {'queryset': Group.objects.with_counts()}, name='index_groups'),
    url(r'^group/(?P<slug>[a-zA-Z/-]+)/$', list_detail.object_detail, group_dict,  name='index_by_group'),
    url(r'^committee/$', list_detail.object_list, {'queryset': Committee.objects.with_counts()}, name='index_committees'),
    url(r'^committee/(?P<slug>[A-Z]+)/$', list_detail.object_detail, committe_dict, name='index_by_committee'),
    url(r'^delegation/$', list_detail.object_list, {'queryset': Delegation.objects.with_counts()}, name='index_delegations'),
    url(r'^delegation/(?P<object_id>[0-9]+)/$', list_detail.object_detail, delegation_dict, name='index_by_delegation'),
    url(r'^party/$', list_detail.object_list, {'queryset': Party.objects.with_counts()}, name='index_parties'),
    url(r'^party/(?P<object_id>[0-9]+)/$', list_detail.object_detail, party_dict,  name='index_by_party'),
    url(r'^floor/$', list_detail.object_list, {'queryset': Building.objects.all().order_by('postcode')}, name='index_floor'),

    url(r'^deputy/(?P<slug>\w+)/$', list_detail.object_detail, mep_dict, name='mep'),
    url(r'^deputy/(?P<slug>\w+)/dataporn/$', list_detail.object_detail, mep_dict_dataporn, name='mep_dataporn'),
    url(r'^deputy/(?P<slug>\w+)/contact$', list_detail.object_detail, mep_contact_dict, name='mep_contact'),
)
urlpatterns += patterns('meps.views',
    url(r'^mep/(?P<ep_id>[0-9]+)/picture.jpg$', 'get_mep_picture',
        name='mep-picture'),
)
