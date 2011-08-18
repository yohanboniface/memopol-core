from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from votes.models import Proposal, Vote, Recommendation, RecommendationData
from reps.models import Representative
from meps.models import MEP

# TODO: refactor those 3 functions, should probably be moved to generic views if possible
def proposal_rep(request, proposal_id, mep_id):
    representative = get_object_or_404(Representative, id=mep_id)
    proposal = get_object_or_404(Proposal, id=proposal_id)
    votes = [Vote.objects.get(representative=representative, recommendation=r)
             if Vote.objects.filter(representative=representative, recommendation=r)
             else {'choice': 'absent', 'recommendation': r, 'representative': representative}
             for r in proposal.recommendation_set.all()]
    context = {'representative': representative, 'proposal': proposal, 'votes': votes}
    return render_to_response('votes/per_rep.html', context, context_instance=RequestContext(request))

def mep_recommendation(request, proposal_id, recommendation_id, recommendation):
    _recommendation = get_object_or_404(Recommendation, id=recommendation_id)
    meps = MEP.objects.filter(vote__recommendation=_recommendation,
                              vote__choice=recommendation)
    return render_to_response("meps/mep_list.html", {'recommendation': _recommendation, 'choice': recommendation, 'object_list' : meps, 'header_template' : 'votes/header_mep_list.html'}, context_instance=RequestContext(request))

class VoteRecommendation(DetailView):
    template_name='votes/recommendation_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(VoteRecommendation, self).get_context_data(**kwargs)
        context['choice_listing'] = True
        context['proposal'] = get_object_or_404(Proposal, id=self.kwargs['proposal_id'])
        return context

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Proposal), name='index'),
    url(r'^import/$', ListView.as_view(model=RecommendationData), name='import'),
    url(r'^import/(?P<pk>\d+)/$', DetailView.as_view(model=RecommendationData), name='import_vote'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<recommendation_id>\d+)/(?P<recommendation>\w+)/$', mep_recommendation, name='recommendation_choice'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/$', VoteRecommendation.as_view(model=Recommendation), name='recommendation'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<mep_id>[a-zA-Z-_]+)/$', proposal_rep, name='rep'),
    url(r'^(?P<pk>[a-zA-Z/-_]+)/$', DetailView.as_view(model=Proposal, context_object_name='vote'), name='detail'),
)
