from django.db import models
from reps.models import Representative
from django.core.urlresolvers import reverse
from memopol2.utils import reify
import search

class Function(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s: %s' % (self.type, self.title and self.title[:15]+'...' or '-')


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    number = models.CharField(max_length=3, primary_key=True)

    def count(self):
        return len(self.mps())

    def mps(self):
        return self.mp_set.filter(active=True)

    def __unicode__(self):
        return self.name


class Circonscription(models.Model):
    number = models.CharField(max_length=31)
    department = models.ForeignKey(Department)

    def __unicode__(self):
        return u'%s - %s' % (self.number, self.department)


class Canton(models.Model):
    name = models.CharField(max_length=511)
    circonscription = models.ForeignKey(Circonscription)

    def __unicode__(self):
        return self.name


class Group(models.Model):
    abbreviation = models.CharField(max_length=31, primary_key=True)
    name = models.CharField(max_length=255)

    def count(self):
        return len(self.mps())

    def mps(self):
        return self.mp_set.filter(active=True)

    def __unicode__(self):
        return self.name


@search.searchable
class MP(Representative):
    active = models.BooleanField()
    birth_department = models.CharField(max_length=255)
    an_id = models.IntegerField()
    an_speeches = models.URLField()
    an_debates = models.URLField(null=True)
    an_commissions = models.URLField()
    an_reports = models.URLField()
    an_questions = models.URLField()
    an_propositions = models.URLField()
    an_webpage = models.URLField()
    functions = models.ManyToManyField(Function, through='FunctionMP')
    profession = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department)
    group = models.ForeignKey(Group)
    group_role = models.CharField(max_length=63, null=True)

    def get_absolute_url(self):
        return reverse('mps:mp', args=(self.id,))

    def scores(self):
        return self.score_set.all()

    @reify
    def phones(self):
        values = []
        for addr in self.address_set.all():
            values.extend(
                [p.number for p in addr.phone_set.filter(type='phone')]
              )
        return values

class FunctionMP(models.Model):
    mp = models.ForeignKey(MP)
    function = models.ForeignKey(Function)
    role = models.CharField(max_length=255)
    mission = models.CharField(max_length=255, null=True)


class Address(models.Model):
    key = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postcode = models.CharField(max_length=31)
    title = models.CharField(max_length=63, null=True)
    mp = models.ForeignKey(MP)


class Phone(models.Model):
    type = models.CharField(max_length=5, choices=((u'phone', u'Phone'), (u'fax', u'Fax')))
    number = models.CharField(max_length=63)
    address = models.ForeignKey(Address)

    def __unicode__(self):
        return '%s: %s' % (self.type, self.number)


class Mandate(models.Model):
    current = models.BooleanField()
    type = models.CharField(max_length=127)
    role = models.CharField(max_length=255, null=True)
    election_date = models.DateField(null=True)
    begin_term = models.DateField(null=True)
    begin_reason = models.CharField(max_length=255, null=True)
    end_term = models.DateField(null=True)
    end_reason = models.CharField(max_length=255, null=True)
    institution = models.CharField(max_length=255, null=True)
    mp = models.ForeignKey(MP)
