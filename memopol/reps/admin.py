# -*- coding: utf-8 -*-
from django.contrib import admin
from memopol.reps import models

class OpinionREP(admin.TabularInline):
    model = models.OpinionREP
    extra = 1

class Opinion(admin.ModelAdmin):
    inlines = [OpinionREP]
admin.site.register(models.Opinion, Opinion)

class WebSite(admin.TabularInline):
    model = models.WebSite
    extra = 1

class Email(admin.TabularInline):
    model = models.Email
    extra = 1

class CV(admin.TabularInline):
    model = models.CV
    extra = 1

class Representative(admin.ModelAdmin):
    inlines = [CV, WebSite, Email]
admin.site.register(models.Representative, Representative)

