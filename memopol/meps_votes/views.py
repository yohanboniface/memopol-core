# -*- coding: utf-8 -*-

from django.db.models import Q
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from memopol.meps.models import MEP
from memopol.votes.models import Proposal, Vote

from memopol.meps.views import optimise_mep_query
from memopol.base.utils import stripdiacritics

class ProposalView(DetailView):
    model = Proposal
    context_object_name = "vote"
    template_name = "meps/proposal_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProposalView, self).get_context_data(**kwargs)
        recommendations = self.object.recommendation_set.all()
        context['vote'].meps = optimise_mep_query(context['vote'].meps, proposal_score=context['vote'])

        # Group subvotes by subject
        subvotes = {}
        subvotes_per_mep = {}
        for subvote in recommendations:
            if not subvote.subject in subvotes:
                subvotes[subvote.subject] = []
            subvotes[subvote.subject].append(subvote)
            # Retrieve all recommendation choices
            positions = Vote.objects.filter(recommendation=subvote).select_related("representative").values('representative_id', 'choice')
            subvotes_per_mep[subvote.pk] = dict((p["representative_id"], p['choice']) for p in positions)

        # Link positions to representatives
        representatives_data = {}
        for mep in context["vote"].meps:
            positions = []
            for subvote in recommendations:
                try:
                    position = subvotes_per_mep[subvote.pk][mep.pk]
                except KeyError:
                    # No proposition for this mep, don't break the order
                    # so use a None value
                    position = None
                finally:
                    positions.append((position, subvote.recommendation))
            representatives_data[mep.pk] = (mep, positions)
        context.update({
            "representatives_data": sorted(representatives_data.values(),
                                           key=lambda x: stripdiacritics(x[0].last_name).lower()),
            "subvotes": subvotes,
        })
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
