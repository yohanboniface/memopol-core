# -*- coding: utf-8 -*-
from django.contrib import admin
from reps import models

class OpinionREP(admin.TabularInline):
    model = models.OpinionREP

class Opinion(admin.ModelAdmin):
    inlines = [OpinionREP]
admin.site.register(models.Opinion, Opinion)

class WebSite(admin.TabularInline):
    model = models.WebSite

class Email(admin.TabularInline):
    model = models.Email

class CV(admin.TabularInline):
    model = models.CV

class Representative(admin.ModelAdmin):
    inlines = [CV, WebSite, Email]
admin.site.register(models.Representative, Representative)

