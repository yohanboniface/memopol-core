from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from memopol.votes.models import Proposal
from memopol.mps.models import MP
from memopol.mps.views import optimize_mp_query


class VoteRecommendation(DetailView):
    template_name='mps/recommendation_detail.html'
    redirect="mps:votes:recommendation"

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
    template_name='mps/mp_list.html'
    redirect="mps:votes:recommendation_choice"

    def get_context_data(self, *args, **kwargs):
        context = super(VoteRecommendationChoice, self).get_context_data(**kwargs)
        context['choice'] = self.kwargs['recommendation']
        context['mps'] = optimize_mp_query(MP.objects.filter(vote__recommendation=self.object,
                                  vote__choice=self.kwargs['recommendation']))
        self.redirect_args += [self.kwargs['recommendation']]
        return context


class ProposalDetailView(DetailView):
    model=Proposal
    context_object_name='vote'
    template_name="mps/proposal_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProposalDetailView, self).get_context_data(**kwargs)
        context["mps"] = optimize_mp_query(context["vote"].mps)
        return context
