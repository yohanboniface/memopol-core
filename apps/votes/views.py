from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView

from meps.models import MEP

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
        context['object_list'] = MEP.objects.at(self.object.datetime.date()).filter(vote__recommendation=self.object,
                                  vote__choice=self.kwargs['recommendation'])
        self.redirect_args += [self.kwargs['recommendation']]
        return context
