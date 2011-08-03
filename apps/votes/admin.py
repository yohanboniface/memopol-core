# -*- coding: utf-8 -*-
from votes import models
from django.contrib import admin

admin.site.register(models.Proposal)
admin.site.register(models.Recommendation)
admin.site.register(models.RecommendationData)
admin.site.register(models.Vote)
admin.site.register(models.Score)
