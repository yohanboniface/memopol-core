from tastypie.resources import ModelResource
from votes.models import Proposal,\
                         Recommendation,\
                         Vote,\
                         Score,\
                         RecommendationData


class ProposalResource(ModelResource):
    class Meta:
        queryset = Proposal.objects.all()


class RecommendationResource(ModelResource):
    class Meta:
        queryset = Recommendation.objects.all()


class VoteResource(ModelResource):
    class Meta:
        queryset = Vote.objects.all()


class ScoreResource(ModelResource):
    class Meta:
        queryset = Score.objects.all()


class RecommendationDataResource(ModelResource):
    class Meta:
        queryset = RecommendationData.objects.all()
