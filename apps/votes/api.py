from tastypie import fields
from tastypie.resources import ModelResource
from votes.models import Proposal,\
                         Recommendation,\
                         Vote,\
                         Score,\
                         RecommendationData


class ProposalResource(ModelResource):
    score_set = fields.ToManyField("votes.api.ScoreResource", "score_set")
    recommendation_set = fields.ToManyField("votes.api.RecommendationResource", "recommendation_set")

    class Meta:
        queryset = Proposal.objects.all()


class RecommendationResource(ModelResource):
    vote_set = fields.ToManyField("votes.api.VoteResource", "vote_set")
    proposal = fields.ForeignKey(ProposalResource, "proposal")

    class Meta:
        queryset = Recommendation.objects.all()


class VoteResource(ModelResource):
    representative = fields.ForeignKey("reps.api.REPRepresentativeResource", "representative")
    recommendation = fields.ForeignKey(RecommendationResource, "recommendation")

    class Meta:
        queryset = Vote.objects.all()


class ScoreResource(ModelResource):
    class Meta:
        queryset = Score.objects.all()


class RecommendationDataResource(ModelResource):
    class Meta:
        queryset = RecommendationData.objects.all()
