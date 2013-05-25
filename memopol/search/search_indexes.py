# -*- coding: utf-8 -*-

from haystack import indexes
from memopol.meps.models import MEP
from memopol.base.utils import stripdiacritics

class MEPIndex(indexes.SearchIndex, indexes.Indexable):
    fulltext = indexes.NgramField(document=True)
    last_name = indexes.CharField()
    group = indexes.CharField(model_attr="group__abbreviation", faceted=True, default="")
    country = indexes.CharField(model_attr="country__code", faceted=True)
    committees = indexes.MultiValueField()
    delegations = indexes.MultiValueField()
    total_score = indexes.FloatField(model_attr="total_score", default=0)
    is_active = indexes.BooleanField(model_attr="active")
    achievements = indexes.MultiValueField()
    bxl_building = indexes.CharField(model_attr="bxl_building__pk", null=True)
    bxl_floor = indexes.CharField(model_attr="bxl_floor", null=True)
    stg_building = indexes.CharField(model_attr="stg_building__pk", null=True)
    stg_floor = indexes.CharField(model_attr="stg_floor", null=True)

    def get_model(self):
        return MEP

    def prepare_committees(self, obj):
        return [c.committee.abbreviation for c in obj.committees_roles.only_current()]

    def prepare_delegations(self, obj):
        return [d.delegation.pk for d in obj.delegations_roles.only_current()]

    def prepare_achievements(self, obj):
        return [a.slug for a in obj.achievements.all()]

    def prepare_fulltext(self, obj):
        return [stripdiacritics(obj.content()), obj.content()]

    def prepare_last_name(self, obj):
        return [stripdiacritics(obj.last_name), ]
