#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Dossier(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    title = models.CharField(max_length=2048, unique=True)
    _date = models.DateField(default=None, null=True, blank=True)

class Committee(models.Model):
    cid = models.CharField(max_length=4)
    title = models.CharField(max_length=512)
    date = models.DateField(default=None, null=True, blank=True)
    dossier = models.ForeignKey(Dossier)
    src = models.CharField(max_length=2048)

class Amendment(models.Model):
    seq = models.IntegerField()
    dossier = models.ForeignKey(Dossier)
    committee = models.ForeignKey(Committee)
    lang = models.CharField(max_length=2 )
    authors = models.TextField()
    new = models.TextField()
    old = models.TextField()
    type = models.CharField(max_length=512)
    location = models.CharField(max_length=1024)

class Score(models.Model):
    am = models.ForeignKey(Amendment)
    user = models.ForeignKey(User)
    score = models.IntegerField()

class Comment(models.Model):
    am = models.ForeignKey(Amendment)
    user = models.ForeignKey(User)
    comment = models.TextField()
    date = models.DateTimeField(default=None, null=True, blank=True)
