from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail

from meps import views
from meps.models import MEP, Country, Group, Committee, Delegation

from reps.models import Party

country_dict = {'queryset': Country.objects.all(), 'slug_field': 'code', 'template_name': 'meps/container_detail.html'}
party_dict = {'queryset': Party.objects.all(), 'template_name': 'meps/container_detail.html'}
group_dict = {'queryset': Group.objects.all(), 'slug_field': 'abbreviation', 'template_name': 'meps/container_detail.html'}
delegation_dict = {'queryset': Delegation.objects.all(), 'template_name': 'meps/container_detail.html'}
committe_dict = {'queryset': Committee.objects.all(), 'slug_field': 'abbreviation', 'template_name': 'meps/container_detail.html'}
mep_dict = {'queryset': MEP.objects.all(), 'slug_field': 'id', 'template_object_name': 'mep'}

urlpatterns = patterns('',
    url(r'^names/$', list_detail.object_list, {'queryset': MEP.objects.filter(active=True)}, name='index_names'),
    url(r'^countries/$', list_detail.object_list, {'queryset': Country.objects.with_counts()}, name='index_countries'),
    url(r'^country/(?P<slug>[a-zA-Z][a-zA-Z])/$', list_detail.object_detail, country_dict, name='index_by_country'),
    url(r'^groups/$', list_detail.object_list, {'queryset': Group.objects.with_counts()}, name='index_groups'),
    url(r'^group/(?P<slug>[a-zA-Z/-]+)/$', list_detail.object_detail, group_dict,  name='index_by_group'),
    url(r'^committees/$', list_detail.object_list, {'queryset': Committee.objects.with_counts()}, name='index_committes'),
    url(r'^committee/(?P<slug>[A-Z]+)/$', list_detail.object_detail, committe_dict, name='index_by_committe'),
    url(r'^delegations/$', list_detail.object_list, {'queryset': Delegation.objects.with_counts()}, name='index_delegations'),
    url(r'^delegation/(?P<object_id>[0-9]+)/$', list_detail.object_detail, delegation_dict, name='index_by_delegation'),
    url(r'^parties/$', list_detail.object_list, {'queryset': Party.objects.with_counts()}, name='index_parties'),
    url(r'^party/(?P<object_id>[0-9]+)/$', list_detail.object_detail, party_dict,  name='index_by_party'),

    url(r'^mep/(?P<slug>\w+)/$', list_detail.object_detail, mep_dict, name='mep'),
    url(r'^mep/(?P<mep_id>\w+)/addposition/$', views.mep_addposition, name='mep_addposition'),

    url(r'^moderation/$', views.moderation, name='moderation'),
    url(r'^moderation/get_unmoderated_positions$', views.moderation_get_unmoderated_positions, name='moderation_get_unmoderated_positions'),
    url(r'^moderation/moderate_position$', views.moderation_moderate_positions, name='moderation_moderate_positions'),
)

