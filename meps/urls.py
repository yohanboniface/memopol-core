from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, TemplateView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse

from meps.models import LocalParty, Country, Group, Committee, Delegation, Organization, Building, MEP
from reps.models import Opinion
from votes.models import Proposal, Vote, Recommendation
from meps.views import VoteRecommendation, VoteRecommendationChoice

from views import BuildingDetailView, MEPView, MEPsFromView, MEPList, PartyView

# TODO: refactor this function, should probably be moved to class based generic views if possible
def proposal_rep(request, proposal_id, mep_id):
    representative = get_object_or_404(MEP, id=mep_id)
    proposal = get_object_or_404(Proposal, id=proposal_id)
    # dirty query because we don't store absent vote
    votes = [Vote.objects.get(representative=representative, recommendation=r)
             if Vote.objects.filter(representative=representative, recommendation=r)
             else {'choice': 'absent', 'recommendation': r, 'representative': representative}
             for r in proposal.recommendation_set.all()]
    context = {'representative': representative, 'proposal': proposal, 'votes': votes}
    return render(request, 'meps/per_mep.html', context)

urlpatterns = patterns('meps.views',
    # those view are *very* expansive. we cache them in RAM for a week
    url(r'^generic/$', 'generic', name="generic"),
    url(r'^query/$', TemplateView.as_view(template_name="meps/query.html"), name="generic"),
    url(r'^filter/(?P<name>[a-z_]+)/$', 'get_filter', name="filter"),
    url(r'^names/$', MEPList.as_view(), name='index_names'),
    url(r'^inactive/$', MEPList.as_view(active=False), name='index_inactive'),
    url(r'^score/$', MEPList.as_view(queryset=MEP.objects.filter(active=True).exclude(total_score__isnull=True).order_by('position'), score_listing=True), name='scores'),

    url(r'^opinion/$', ListView.as_view(queryset=Opinion.with_meps_count().order_by('-_date').select_related('_author')), name='index_opinions'),
    url(r'^opinion/(?P<pk>[0-9]+)/$', DetailView.as_view(model=Opinion, template_name="meps/opinion_detail.html"), name='index_by_opinions'),
    url(r'^organization/$', ListView.as_view(queryset=Organization.with_meps_count()), name='index_organizations'),
    url(r'^organization/(?P<pk>[0-9]+)/$', MEPsFromView.as_view(model=Organization, organization_role=True), name='index_by_organization'),
    url(r'^country/$', ListView.as_view(queryset=Country.with_meps_count()), name='index_countries'),
    url(r'^country/(?P<slug>[a-zA-Z][a-zA-Z])/$', MEPsFromView.as_view(model=Country, slug_field='code', hidden_fields=['country'], named_header="meps/country_header.html"), name='index_by_country'),
    url(r'^group/$', ListView.as_view(queryset=Group.ordered_by_meps_count()), name='index_groups'),
    url(r'^group/(?P<slug>[a-zA-Z/-]+)/$', MEPsFromView.as_view(model=Group, hidden_fields=['group'], slug_field="abbreviation", named_header="meps/group_header.html", group_role=True),  name='index_by_group'),
    url(r'^committee/$', ListView.as_view(queryset=Committee.ordered_by_meps_count()), name='index_committees'),
    url(r'^committee/(?P<slug>[A-Z]+)/$', MEPsFromView.as_view(model=Committee, slug_field="abbreviation", committee_role=True), name='index_by_committee'),
    url(r'^delegation/$', ListView.as_view(queryset=Delegation.with_meps_count()), name='index_delegations'),
    url(r'^delegation/(?P<pk>[0-9]+)/$', MEPsFromView.as_view(model=Delegation, delegation_role=True), name='index_by_delegation'),
    url(r'^party/$', ListView.as_view(queryset=LocalParty.with_meps_count().order_by('country').select_related('country')), name='index_parties'),
    url(r'^party/(?P<pk>[0-9]+)-(?P<slugified_name>[0-9a-z\-]*)/$', PartyView.as_view(),  name='index_by_party'),
    url(r'^floor/$', ListView.as_view(queryset=Building.objects.order_by('postcode')), name='index_floor'),
    url(r'^floor/brussels/(?P<pk>\w+)/(?P<floor>\w+)/$', BuildingDetailView.as_view(), name='bxl_floor'),
    url(r'^floor/strasbourg/(?P<pk>\w+)/(?P<floor>\w+)/$', BuildingDetailView.as_view(), name='stg_floor'),

    url(r'^vote/$', ListView.as_view(queryset=Proposal.objects.filter(institution="EU").order_by('-_date')), name='index_votes'),
    url(r'^vote/(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/(?P<recommendation>\w+)/$', VoteRecommendationChoice.as_view(model=Recommendation), name='recommendation_choice'),
    url(r'^vote/(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/$', VoteRecommendation.as_view(model=Recommendation, template_name="meps/recommendation_detail.html"), name='recommendation'),
    url(r'^vote/(?P<pk>[a-zA-Z/-_]+)/dataporn/$', DetailView.as_view(model=Proposal, context_object_name='vote', template_name="meps/proposal_dataporn.html"), name='vote_dataporn'),
    url(r'^vote/(?P<proposal_id>[a-zA-Z/-_]+)/(?P<mep_id>.+)/$', proposal_rep, name='votes_mep'),
    url(r'^vote/(?P<pk>[a-zA-Z/-_]+)/$', DetailView.as_view(model=Proposal, context_object_name='vote', template_name="meps/proposal_detail.html"), name='vote'),

    url(r'^votes/$', lambda request: redirect(reverse("meps:index_votes"))),

    url(r'^deputy/(?P<pk>\w+)/$', MEPView.as_view(), name='mep'),
    url(r'^deputy/(?P<pk>\w+)/dataporn/$', MEPView.as_view(template_name="meps/dataporn.html"), name='mep_dataporn'),
    url(r'^deputy/(?P<pk>\w+)/contact$', MEPView.as_view(template_name="meps/mep_contact.html"), name='mep_contact'),
)

urlpatterns += patterns('meps.views',
    url(r'^mep/(?P<ep_id>[0-9]+)/picture.jpg$', 'get_mep_picture',
        name='mep-picture'),
)
