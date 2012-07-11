# -*- coding:Utf-8 -*-
import json
from django.db import models
from django.db.models import Avg

from utils import clean_all_trends
from reps.models import Representative
from meps.models import MEP, Group, Country
from mps.models import MP
from memopol2.utils import color, reify
from django.core.urlresolvers import reverse


class Proposal(models.Model):
    id = models.CharField(max_length=63, primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    ponderation = models.IntegerField(default=1)
    short_name = models.CharField(max_length=25, default=None, null=True)
    institution = models.CharField(max_length=63, choices=((u'EU', 'european parliament'), (u'FR', 'assemblée nationale française')))
    _date = models.DateField(default=None, null=True, blank=True)

    def get_absolute_url(self):
        if self.institution == "FR":
            return reverse("mps:vote", args=[self.id])
        return reverse("meps:vote", args=[self.id])

    @property
    def groups(self):
        groups = Group.objects.filter(groupmep__mep__score__proposal=self, groupmep__begin__lte=self.date, groupmep__end__gte=self.date).distinct().order_by('abbreviation')
        if not groups:
            return Group.objects.filter(groupmep__mep__score__proposal=self).distinct().order_by('abbreviation')
        return groups

    @property
    def countries(self):
        countries = Country.objects.filter(countrymep__mep__score__proposal=self, countrymep__begin__lte=self.date, countrymep__end__gte=self.date).distinct().order_by('code')
        if not countries:
            return Country.objects.filter(countrymep__mep__score__proposal=self).distinct().order_by('code')
        return countries

    @property
    def date(self):
        if self._date is None:
            self._date = self.recommendation_set.all()[0].datetime.date()
            self.save()
        return self._date

    def save(self, *args, **kwargs):
        # if I'm modifyed and not created
        if Proposal.objects.filter(id=self.id):
            clean_all_trends()
        super(Proposal, self).save(*args, **kwargs)

    @reify
    def meps(self):
        return MEP.objects.filter(score__proposal=self)

    @reify
    def mps(self):
        return MP.objects.filter(vote__recommendation__proposal=self).distinct()

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
    _significant_votes = models.IntegerField(default=None, null=True, blank=True)
    _for_count = models.IntegerField(default=None, null=True, blank=True)
    _against_count = models.IntegerField(default=None, null=True, blank=True)
    _abstention_count = models.IntegerField(default=None, null=True, blank=True)
    _absent_count = models.IntegerField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        # if I'm modifyed and not created
        if Recommendation.objects.filter(pk=self.pk):
            clean_all_trends()
        super(Recommendation, self).save(*args, **kwargs)

    def meps_with_votes(self):
        for mep in MEP.objects.filter(vote__recommendation=self):
            yield mep, mep.vote_set.filter(recommendation=self)[0].choice # bad bad bad, filter should disapear soon for a get

    def mps_with_votes(self):
        for mp in MP.objects.filter(vote__recommendation=self):
            yield mp, mp.vote_set.get(recommendation=self).choice

    @reify
    def significant_votes(self):
        if not self._significant_votes:
            self._significant_votes = self.vote_set.all().exclude(choice='absent').exclude(choice='abstention').count()
            self.save()
        return self._significant_votes

    def __unicode__(self):
        return self.subject

    class MetaClass:
        ordering = ['datetime']

class Vote(models.Model):
    choice = models.CharField(max_length=15, choices=((u'for', u'for'), (u'against', u'against'), (u'abstention', u'abstention'), (u'absent', u'absent')))
    name = models.CharField(max_length=127)
    recommendation = models.ForeignKey(Recommendation)
    representative = models.ForeignKey(Representative, null=True)

    def save(self, *args, **kwargs):
        # if I'm modifyed and not created
        if Recommendation.objects.filter(pk=self.pk):
            clean_all_trends()
        super(Vote, self).save(*args, **kwargs)

    class Meta:
        ordering = ["choice"]

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.choice)


class Score(models.Model):
    value = models.FloatField()
    representative = models.ForeignKey(Representative)
    proposal = models.ForeignKey(Proposal)
    date = models.DateField()

    def save(self, *args, **kwargs):
        # if I'm modifyed and not created
        if Recommendation.objects.filter(pk=self.pk):
            clean_all_trends()
        super(Score, self).save(*args, **kwargs)

    class Meta:
        ordering = ['date']

    @property
    def color(self):
        red, green, _ = color(self.value)
        return "rgb(%d, %d, 0)" % (red, green)

    @property
    def color_tuple(self):
        return color(self.value)

    @property
    def of_country(self):
        return Score.objects.filter(representative__mep__countrymep__country=self.representative.mep.country, proposal=self.proposal).aggregate(Avg('value'))['value__avg']

    @property
    def of_group(self):
        if self.representative.mep.groups.count():
            return Score.objects.filter(representative__mep__groupmep__group=self.representative.mep.group, proposal=self.proposal).aggregate(Avg('value'))['value__avg']
        else:
            return None

    @property
    def of_ep(self):
        return Score.objects.filter(proposal=self.proposal).aggregate(Avg('value'))['value__avg']


class RecommendationData(models.Model):
    proposal_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    imported = models.BooleanField(default=False)
    date = models.DateTimeField()
    data = models.TextField()
    recommendation = models.OneToOneField(Recommendation, null=True)

    def data_pretty(self):
        return json.dumps(json.loads(self.data), sort_keys=False, indent=4)

    class Meta:
        ordering = ['date', 'proposal_name']
