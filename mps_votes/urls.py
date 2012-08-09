from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render

from mps.models import MP
from votes.models import Proposal, Vote, Recommendation
from views import VoteRecommendation, VoteRecommendationChoice, ProposalDetailView


def proposal_rep(request, proposal_id, mp_id):
    representative = get_object_or_404(MP, id=mp_id)
    proposal = get_object_or_404(Proposal, id=proposal_id)
    # dirty query because we don't store absent vote
    votes = [Vote.objects.get(representative=representative, recommendation=r)
             if Vote.objects.filter(representative=representative, recommendation=r)
             else {'choice': 'absent', 'recommendation': r, 'representative': representative}
             for r in proposal.recommendation_set.all()]
    context = {'representative': representative, 'proposal': proposal, 'votes': votes}
    return render(request, 'meps/per_mep.html', context)


urlpatterns = patterns('mps.views',
    url(r'^$', ListView.as_view(queryset=Proposal.objects.filter(institution="FR").order_by('-_date')), name='index_votes'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/(?P<recommendation>[0-9\w.]+)/$', VoteRecommendationChoice.as_view(model=Recommendation), name='recommendation_choice'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/$', VoteRecommendation.as_view(model=Recommendation, template_name="mps/recommendation_detail.html"), name='recommendation'),
    url(r'^(?P<pk>[a-zA-Z/-_]+)/dataporn/$', DetailView.as_view(model=Proposal, context_object_name='vote', template_name="mps/proposal_dataporn.html"), name='vote_dataporn'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<mp_id>.+)/$', proposal_rep, name='votes_mp'),
    url(r'^(?P<pk>[a-zA-Z/-_]+)/$', ProposalDetailView.as_view(), name='vote'),
)
