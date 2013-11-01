from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page

from memopol.meps.models import LocalParty, Country, Group, Committee, Delegation, Organization, Building, MEP
from memopol.reps.models import Opinion

from .views import (MEPView, MEPsFromView, MEPList, PartyView,
                    RedirectToSearch, RedirectFloorListToSearch,
                    RedirectToMepFromEPID)

urlpatterns = patterns('memopol.meps.views',
    url(r'^opinion/$', ListView.as_view(queryset=Opinion.with_meps_count().order_by('-_date').select_related('_author')), name='index_opinions'),
    url(r'^opinion/(?P<pk>[0-9]+)/$', MEPsFromView.as_view(model=Opinion, template_name="meps/opinion_detail.html"), name='index_by_opinions'),
    url(r'^organization/$', ListView.as_view(queryset=Organization.with_meps_count()), name='index_organizations'),
    url(r'^organization/(?P<pk>[0-9]+)/$', MEPsFromView.as_view(model=Organization, organization_role=True), name='index_by_organization'),
    url(r'^country/$', ListView.as_view(queryset=Country.with_meps_count()), name='index_countries'),
    url(r'^country/(?P<value>[a-zA-Z][a-zA-Z])/$', RedirectToSearch.as_view(filter="country"), name='index_by_country'),
    url(r'^group/$', ListView.as_view(queryset=Group.ordered_by_meps_count()), name='index_groups'),
    url(r'^group/(?P<value>[a-zA-Z/-]+)/$', RedirectToSearch.as_view(filter="group"), name='index_by_group'),
    url(r'^committee/$', ListView.as_view(queryset=Committee.ordered_by_meps_count()), name='index_committees'),
    url(r'^committee/(?P<value>[A-Z]+)/$', RedirectToSearch.as_view(filter="committees"), name='index_by_committee'),
    url(r'^delegation/$', ListView.as_view(queryset=Delegation.with_meps_count()), name='index_delegations'),
    url(r'^delegation/(?P<value>[0-9]+)/$', RedirectToSearch.as_view(filter="delegations"), name='index_by_delegation'),
    url(r'^party/$', ListView.as_view(queryset=LocalParty.with_meps_count().order_by('country').select_related('country')), name='index_parties'),
    url(r'^party/(?P<pk>[0-9]+)-(?P<slugified_name>[0-9a-z\-]*)/$', PartyView.as_view(),  name='index_by_party'),
    url(r'^floor/$', ListView.as_view(queryset=Building.objects.order_by('postcode')), name='index_floor'),
    url(r'^floor/brussels/(?P<building>\w+)/(?P<floor>\w+)/$', RedirectFloorListToSearch.as_view(city="bxl"), name='bxl_floor'),
    url(r'^floor/strasbourg/(?P<building>\w+)/(?P<floor>\w+)/$', RedirectFloorListToSearch.as_view(city="stg"), name='stg_floor'),

    url(r'^vote/', include('memopol.meps_votes.urls', namespace="votes", app_name="meps_votes")),

    url(r'^votes/$', lambda request: redirect(reverse("meps:votes:index_votes"))),

    url(r'^deputy_from_ep_id/(?P<ep_id>\d+)/$', RedirectToMepFromEPID.as_view(), name='mep'),
    url(r'^deputy/(?P<pk>\w+)/$', cache_page(MEPView.as_view(), 60 * 60 * 24), name='mep'),
    url(r'^deputy/(?P<pk>\w+)/dataporn/$', cache_page(MEPView.as_view(template_name="meps/dataporn.html"), 60 * 60 * 24), name='mep_dataporn'),
    url(r'^deputy/(?P<pk>\w+)/contact$', cache_page(MEPView.as_view(template_name="meps/mep_contact.html"), 60 * 60 * 24), name='mep_contact'),
)

urlpatterns += patterns('memopol.meps.views',
    url(r'^mep/(?P<ep_id>[0-9]+)/picture.jpg$', 'get_mep_picture',
        name='mep-picture'),
)
