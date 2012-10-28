from django.db import models
from memopol.base.utils import reify
from memopol.meps.models import MEP


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
    intro = models.TextField(blank=True)
    details = models.TextField(blank=True)

    class Admin:
        pass

    def __unicode__(self):
        return u"%s" % (self.title)


class Debriefing(models.Model):
    CONTACT_TYPES = (
        ('Personal', 'Personal'),
        ('Phone', 'Phone'),
        ('Email', 'Email'),
        ('FAX', 'FAX'),
        ('Letter', 'Letter'),
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
    usercontact = models.CharField(max_length=1024, null=True)
    when = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    valid = models.CharField(max_length=64, blank=True)

    class Admin:
        pass
