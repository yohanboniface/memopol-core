from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render

from memopol.votes.models import Proposal, Recommendation, Vote
from memopol.meps.models import MEP

from .views import VoteRecommendation, VoteRecommendationChoice, ProposalView


def proposal_rep(request, proposal_id, mep_id):
    representative = get_object_or_404(MEP, id=mep_id)
    proposal = get_object_or_404(Proposal, id=proposal_id)

    votes = list(Vote.objects.filter(representative=representative, recommendation__proposal=proposal).select_related('recommendation'))
    # we don't store abstent votes so we have to guess them
    # we need a dummy object for the key of the sorted bellow
    votes += [type('DummyVote', (object,), {'choice': 'absent', 'recommendation': x, 'representative': representative}) for x in Recommendation.objects.filter(proposal=proposal).exclude(vote__representative=representative)]

    # recreate default ordering
    votes = sorted(votes, key=lambda x: x.recommendation.datetime)

    context = {'representative': representative, 'proposal': proposal, 'votes': votes}
    return render(request, 'meps/per_mep.html', context)


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset=Proposal.objects.filter(institution="EU").order_by('-_date')), name='index_votes'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/(?P<recommendation>\w+)/$', VoteRecommendationChoice.as_view(model=Recommendation), name='recommendation_choice'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/$', VoteRecommendation.as_view(model=Recommendation, template_name="meps/recommendation_detail.html"), name='recommendation'),
    url(r'^(?P<pk>[a-zA-Z/-_]+)/dataporn/$', DetailView.as_view(model=Proposal, context_object_name='vote', template_name="meps/proposal_dataporn.html"), name='vote_dataporn'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<mep_id>.+)/$', proposal_rep, name='votes_mep'),
    url(r'^(?P<pk>[a-zA-Z/-_]+)/$', ProposalView.as_view(), name='vote'),
)
