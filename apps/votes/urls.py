from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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

class VoteRecommendation(DetailView):
    template_name='votes/recommendation_detail.html'
    redirect="votes:recommendation"

    def get_context_data(self, *args, **kwargs):
        context = super(VoteRecommendation, self).get_context_data(**kwargs)
        context['choice_listing'] = True
        context['proposal'] = self.object.proposal
        self.redirect_args = [self.object.proposal.id, self.object.id]
        return context

    def render_to_response(self, context):
        if self.kwargs["proposal_id"] != self.object.proposal.id:
            return HttpResponseRedirect(reverse(self.redirect, args=self.redirect_args))
        return DetailView.render_to_response(self, context)

class VoteRecommendationChoice(VoteRecommendation):
    template_name='meps/mep_list.html'
    redirect="votes:recommendation_choice"

    def get_context_data(self, *args, **kwargs):
        context = super(VoteRecommendationChoice, self).get_context_data(**kwargs)
        context['choice'] = self.kwargs['recommendation']
        context['header_template'] = 'votes/header_mep_list.html'
        context['object_list'] = MEP.objects.filter(vote__recommendation=self.object,
                                  vote__choice=self.kwargs['recommendation'])
        self.redirect_args += [self.kwargs['recommendation']]
        return context

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Proposal), name='index'),
    url(r'^import/$', ListView.as_view(model=RecommendationData), name='import'),
    url(r'^import/(?P<pk>\d+)/$', DetailView.as_view(model=RecommendationData), name='import_vote'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/(?P<recommendation>\w+)/$', VoteRecommendationChoice.as_view(model=Recommendation), name='recommendation_choice'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<pk>\d+)/$', VoteRecommendation.as_view(model=Recommendation), name='recommendation'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<mep_id>[a-zA-Z-_]+)/$', proposal_rep, name='rep'),
    url(r'^(?P<pk>[a-zA-Z/-_]+)/$', DetailView.as_view(model=Proposal, context_object_name='vote'), name='detail'),
)
