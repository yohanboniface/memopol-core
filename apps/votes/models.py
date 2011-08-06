import json
from django.db import models
from django.db.models import Avg
from reps.models import Representative

class Proposal(models.Model):
    id = models.CharField(max_length=63, primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    ponderation = models.IntegerField(default=1)

    @property
    def date(self):
        return self.recommendation_set.all()[0].datetime.date()

    def __unicode__(self):
        return self.title


class Recommendation(models.Model):
    datetime = models.DateTimeField()
    subject = models.CharField(max_length=255)
    part = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    weight = models.IntegerField(null=True)
    proposal = models.ForeignKey(Proposal)
    recommendation = models.CharField(max_length=15, choices=((u'against', u'against'), (u'for', u'for')), null=True)

    def __unicode__(self):
        return self.subject

class Vote(models.Model):
    choice = models.CharField(max_length=15, choices=((u'for', u'for'), (u'against', u'against'), (u'abstention', u'abstention')))
    name = models.CharField(max_length=127)
    recommendation = models.ForeignKey(Recommendation)
    representative = models.ForeignKey(Representative, null=True)

    class Meta:
        ordering = ["choice"]

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.choice)


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
    def color_tuple(self):
        colors = 255
        val = int(3 * colors * (self.value/100))
        red = green = colors
        if val < colors:
            green = int(2/3 * val)
        elif val < 2 * colors:
            green = int(2 / 3 * colors + 1 / 3 * (val / 2 - colors))
        else:
            red = 3 * colors - val
        return (red / 255., green / 255., 0)

    @property
    def of_country(self):
        return Score.objects.filter(representative__mep__countrymep__country=self.representative.mep.country, proposal=self.proposal).aggregate(Avg('value'))['value__avg']

    @property
    def of_group(self):
        return Score.objects.filter(representative__mep__groupmep__group=self.representative.mep.group, proposal=self.proposal).aggregate(Avg('value'))['value__avg']

    @property
    def of_ep(self):
        return Score.objects.filter(proposal=self.proposal).aggregate(Avg('value'))['value__avg']


class RecommendationData(models.Model):
    proposal_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    imported = models.BooleanField(default=False)
    date = models.DateField()
    data = models.TextField()
    recommendation = models.OneToOneField(Recommendation, null=True)

    def data_pretty(self):
        return json.dumps(json.loads(self.data), sort_keys=False, indent=4)
