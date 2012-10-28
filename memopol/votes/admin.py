# -*- coding: utf-8 -*-
from django.contrib import admin

from memopol.votes import models

admin.site.register(models.Proposal)
admin.site.register(models.Recommendation)
admin.site.register(models.RecommendationData)
admin.site.register(models.Vote)
admin.site.register(models.Score)
