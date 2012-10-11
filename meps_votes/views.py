from django.db.models import Q
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from meps.models import MEP
from votes.models import Proposal

from meps.views import optimise_mep_query


class ProposalView(DetailView):
    model = Proposal
    context_object_name = "vote"
    template_name = "meps/proposal_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProposalView, self).get_context_data(**kwargs)
        context["vote"].meps = optimise_mep_query(context["vote"].meps, Q(mep__score__proposal=context["vote"]), Q(representative__score__proposal=context["vote"]), proposal_score=context["vote"])
        return context


class VoteRecommendation(DetailView):
    template_name = 'meps/recommendation_detail.html'
    redirect = "meps:votes:recommendation"

    def get_context_data(self, *args, **kwargs):
        context = super(VoteRecommendation, self).get_context_data(**kwargs)
        context['choice_listing'] = True
        context['proposal'] = self.object.proposal
        context['meps_with_votes'] = self.meps_with_votes
        self.redirect_args = [self.object.proposal.id, self.object.id]
        return context

    def meps_with_votes(self):
        for mep in optimise_mep_query(MEP.objects.filter(vote__recommendation=self.object), Q(mep__score__proposal=self.object.proposal), Q(representative__score__proposal=self.object.proposal), choice_on_recommendation=self.object):
            yield mep, mep.choice  # bad bad bad, filter should disapear soon for a get

    def render_to_response(self, context):
        if self.kwargs["proposal_id"] != self.object.proposal.id:
            return HttpResponseRedirect(reverse(self.redirect, args=self.redirect_args))
        return DetailView.render_to_response(self, context)


class VoteRecommendationChoice(VoteRecommendation):
    template_name = 'meps/mep_list.html'
    redirect = "meps:votes:recommendation_choice"

    def get_context_data(self, *args, **kwargs):
        context = super(VoteRecommendationChoice, self).get_context_data(**kwargs)
        context['choice'] = self.kwargs['recommendation']
        context['header_template'] = 'votes/header_mep_list.html'
        context['object_list'] = optimise_mep_query(MEP.objects.filter(vote__recommendation=self.object,
                                                                       vote__choice=self.kwargs['recommendation']),
                                                    Q(mep__vote__recommendation=self.object, mep__vote__choice=self.kwargs['recommendation']),
                                                    Q(representative__vote__recommendation=self.object, representative__vote__choice=self.kwargs['recommendation']))
        self.redirect_args += [self.kwargs['recommendation']]
        return context
