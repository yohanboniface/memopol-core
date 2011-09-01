from django.db import models
from django.core.urlresolvers import reverse
from memopol2.utils import reify
from datetime import date
from snippets import snippet
from meps.models import MEP

class MEPScore(models.Model):
    campaign = models.ForeignKey('Campaign')
    mep = models.ForeignKey(MEP)
    score = models.IntegerField(default=0)

    class Admin:
        pass

    @reify
    def instance(self):
        return self.score

    def __unicode__(self):
        return u"%d %s" % (self.score, self.mep)

class ScoreRule(models.Model):
    campaign = models.ForeignKey('Campaign')
    rule = models.CharField(max_length=4096)
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Admin:
        pass

    @reify
    def instance(self):
        return self.score

class Campaign(models.Model):
    title = models.CharField(max_length=1024, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True, blank=True)

    class Admin:
        pass

    def __unicode__(self):
        return u"%s" % (self.title)


class Debriefing(models.Model):
    CONTACT_TYPES = (
        ('I', 'Personal'),
        ('P', 'Phone'),
        ('E', 'Email'),
        ('F', 'FAX'),
        ('L', 'Letter'),
    )
    RESPONSES = (
        ('-', 'Negative'),
        ('0', 'Neutral'),
        ('+', 'Positive'),
        ('?', 'No contact'),
    )
    campaign = models.ForeignKey(Campaign)
    mep = models.ForeignKey(MEP)
    type = models.CharField(max_length=1, choices=CONTACT_TYPES)
    response = models.CharField(max_length=1, choices=RESPONSES)
    when = models.DateTimeField()
    text = models.TextField(blank=True)
