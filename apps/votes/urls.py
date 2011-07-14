from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from votes.models import Proposal, Vote, Recommendation
from reps.models import Representative
from meps.models import MEP

def proposal_rep(request, proposal_id, mep_id):
    representative = get_object_or_404(Representative, id=mep_id)
    proposal = get_object_or_404(Proposal, id=proposal_id)
    votes = [Vote.objects.get(representative=representative, recommendation=r) for r in proposal.recommendation_set.all()]
    context = {'representative': representative, 'proposal': proposal, 'votes': votes}
    return render_to_response('votes/per_rep.html', context, context_instance=RequestContext(request))

def mep_recommendation(request, proposal_id, recommendation_id, recommendation):
    meps = MEP.objects.filter(vote__recommendation=get_object_or_404(Recommendation, id=recommendation_id),
                              vote__choice=recommendation)
    return render_to_response("meps/mep_list.html", {'object_list' : meps})

def vote_recommendation(request, proposal_id, recommendation_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)
    return render_to_response("votes/recommendation_detail.html",
                              {'proposal': proposal, 'recommendation': recommendation})

urlpatterns = patterns('',
    url(r'^$', list_detail.object_list, {'queryset': Proposal.objects.all()}, name='index'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<recommendation_id>\d+)/(?P<recommendation>\w+)/$', mep_recommendation, name='recommendation_choice'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<recommendation_id>\d+)/$', vote_recommendation, name='recommendation'),
    url(r'^(?P<proposal_id>[a-zA-Z/-_]+)/(?P<mep_id>[a-zA-Z-_]+)/$', proposal_rep, name='rep'),
    url(r'^(?P<object_id>[a-zA-Z/-_]+)/$', list_detail.object_detail, {'queryset': Proposal.objects.all(), 'template_object_name': 'vote'}, name='detail'),
)
