# -*- coding: utf-8 -*-
from django.contrib import admin
from memopol.mps import models


class FunctionMP(admin.TabularInline):
    model = models.FunctionMP
    extra = 1

class Address(admin.TabularInline):
    model = models.Address
    extra = 1

class Mandate(admin.TabularInline):
    model = models.Mandate
    extra = 1


class MP(admin.ModelAdmin):
    search_fields = ['last_name']
    list_display = ['last_name', 'first_name', 'department', 'group']
    list_filter = ['group', 'department']
    inlines = [Address, FunctionMP, Mandate]

admin.site.register(models.MP, MP)

class Canton(admin.TabularInline):
    model = models.Canton
    extra = 1

class CirconscriptionAdmin(admin.ModelAdmin):
    inlines = [Canton]

admin.site.register(models.Circonscription, CirconscriptionAdmin)

class Circonscription(admin.TabularInline):
    model = models.Circonscription
    extra = 1

class Department(admin.ModelAdmin):
    inlines = [Circonscription]

admin.site.register(models.Department, Department)
admin.site.register(models.Canton)

