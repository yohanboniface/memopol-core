# -*- coding: utf-8 -*-

from haystack import indexes
from meps.models import MEP


class MEPIndex(indexes.SearchIndex, indexes.Indexable):
    fulltext = indexes.CharField(document=True, model_attr="content")
    group = indexes.CharField(model_attr="group__abbreviation", faceted=True)
    country = indexes.CharField(model_attr="country__code", faceted=True)
    committees = indexes.MultiValueField()
    total_score = indexes.FloatField(model_attr="total_score", default=0)
    is_active = indexes.BooleanField(model_attr="active")

    def get_model(self):
        return MEP

    def prepare_committees(self, obj):
        return [c.abbreviation for c in obj.committees.all()]
