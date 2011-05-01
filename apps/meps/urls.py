from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail

from meps import views
from meps.models import MEP, Country, Group, Committe, Deleguation, Party

country_dict = {'queryset': Country.objects.all(), 'slug_field':'code', 'template_name' :'meps/container_detail.html' }
party_dict = {'queryset': Party.objects.all(), 'template_name' :'meps/container_detail.html' }
group_dict = {'queryset': Group.objects.all(), 'slug_field':'abbreviation', 'template_name' :'meps/container_detail.html' }
deleguation_dict = {'queryset': Deleguation.objects.all(), 'template_name' :'meps/container_detail.html' }
committe_dict = {'queryset': Committe.objects.all(), 'slug_field':'abbreviation', 'template_name' :'meps/container_detail.html' }

urlpatterns = patterns('',
    url(r'^names/$', list_detail.object_list, {'queryset': MEP.objects.filter(active=True)}, name='index_names'),
    url(r'^countries/$', list_detail.object_list, {'queryset': Country.objects.all()}, name='index_countries'),
    url(r'^country/(?P<slug>[a-zA-Z][a-zA-Z])/$', list_detail.object_detail, country_dict, name='index_by_country'),
    url(r'^groups/$', list_detail.object_list, {'queryset': Group.objects.all()}, name='index_groups'),
    url(r'^group/(?P<slug>[a-zA-Z/-]+)/$', list_detail.object_detail, group_dict,  name='index_by_group'),
    url(r'^committes/$', list_detail.object_list, {'queryset': Committe.objects.all()}, name='index_committes'),
    url(r'^committe/(?P<slug>[A-Z]+)/$', list_detail.object_detail, committe_dict, name='index_by_committe'),
    url(r'^deleguations/$', list_detail.object_list, {'queryset': Deleguation.objects.all()}, name='index_deleguations'),
    url(r'^deleguation/(?P<object_id>[0-9]+)/$', list_detail.object_detail, deleguation_dict, name='index_by_deleguation'),
    url(r'^parties/$', list_detail.object_list, {'queryset': Party.objects.all()}, name='index_parties'),
    url(r'^party/(?P<object_id>[0-9]+)/$', list_detail.object_detail, party_dict,  name='index_by_party'),

    url(r'^mep/(?P<mep_id>\w+)/$', views.mep, name='mep'),
    url(r'^mep/(?P<mep_id>\w+)/raw/$', views.mep_raw, name='mep_raw'),
    url(r'^mep/(?P<mep_id>\w+)/json/$', views.mep_json, name='mep_json'),
    url(r'^mep/(?P<mep_id>\w+)/addposition/$', views.mep_addposition, name='mep_addposition'),

    url(r'^moderation/$', views.moderation, name='moderation'),
    url(r'^moderation/get_unmoderated_positions$', views.moderation_get_unmoderated_positions, name='moderation_get_unmoderated_positions'),
    url(r'^moderation/moderate_position$', views.moderation_moderate_positions, name='moderation_moderate_positions'),
)

