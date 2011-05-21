from django.db import models
from reps.models import Representative

class Proposal(models.Model):
    id = models.CharField(max_length=63, primary_key=True)
    title = models.CharField(max_length=255, unique=True)

class Recommendation(models.Model):
    datetime = models.DateTimeField()
    subject = models.CharField(max_length=255)
    part = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    weight = models.IntegerField(null=True)
    proposal = models.ForeignKey(Proposal)
    recommendation = models.CharField(max_length=15, choices=((u'against', u'against'), (u'for', u'for')), null=True)

class Vote(models.Model):
    choice = models.CharField(max_length=15, choices=((u'for', u'for'), (u'against', u'against'), (u'abstention', u'abstention')))
    name = models.CharField(max_length=127)
    recommendation = models.ForeignKey(Recommendation)
    representative = models.ForeignKey(Representative, null=True)
