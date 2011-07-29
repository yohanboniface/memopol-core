import json
from django.db import models
from django.db.models import Avg
from reps.models import Representative

class Proposal(models.Model):
    id = models.CharField(max_length=63, primary_key=True)
    title = models.CharField(max_length=255, unique=True)

    @property
    def date(self):
        return self.recommendation_set.all()[0].datetime.date()


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

    class Meta:
        ordering = ["choice"]


class Score(models.Model):
    value = models.FloatField()
    representative = models.ForeignKey(Representative)
    proposal = models.ForeignKey(Proposal)
    date = models.DateField()

    class Meta:
        ordering = ['date']

    @property
    def color(self):
        red = 255 - self.value
        green = self.value * 2.55
        return "rgb(%d, %d, 0)" % (red, green)

    @property
    def of_country(self):
        return Score.objects.filter(representative__mep__countrymep__country=self.representative.mep.country, proposal=self.proposal).aggregate(Avg('value'))['value__avg']


class RecommendationData(models.Model):
    proposal_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    imported = models.BooleanField(default=False)
    date = models.DateField()
    data = models.TextField()
    recommendation = models.OneToOneField(Recommendation, null=True)

    def data_pretty(self):
        return json.dumps(json.loads(self.data), sort_keys=False, indent=4)
