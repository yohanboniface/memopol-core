# -*- coding: utf-8 -*-

from haystack import indexes
from memopol.meps.models import MEP


class MEPIndex(indexes.SearchIndex, indexes.Indexable):
    fulltext = indexes.CharField(document=True, model_attr="content")
    group = indexes.CharField(model_attr="group__abbreviation", faceted=True, default="")
    country = indexes.CharField(model_attr="country__code", faceted=True)
    committees = indexes.MultiValueField()
    delegations = indexes.MultiValueField()
    total_score = indexes.FloatField(model_attr="total_score", default=0)
    is_active = indexes.BooleanField(model_attr="active")
    achievements = indexes.MultiValueField()

    def get_model(self):
        return MEP

    def prepare_committees(self, obj):
        return [c.abbreviation for c in obj.committees.all()]

    def prepare_delegations(self, obj):
        return [d.pk for d in obj.delegations.all()]

    def prepare_achievements(self, obj):
        return [a.slug for a in obj.achievements.all()]
