# -*- coding:Utf-8 -*-
from datetime import date

from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings
from django.db import models
from django.db.models import Count, Q
from memopol.base.utils import reify
from snippets import snippet
from memopol import meps
from memopol import mps


class RepsContainerManager(models.Manager):
    """ Manager for models to which the representative model has a foreign key"""
    def with_counts(self):
        """ Return the models with a count property, with the count of active Reps """
        return self.get_query_set().filter(representative__mep__active=True).annotate(count=models.Count('representative'))


class Party(models.Model):
    name = models.CharField(max_length=255)
    objects = RepsContainerManager()

    def __unicode__(self):
        return self.name
    content = __unicode__

    def get_absolute_url(self):
        return reverse('meps:index_by_party', args=(self.id, slugify(self.name)))

    @property
    def meps(self):
        return meps.models.MEP.objects.filter(partyrepresentative__party=self, active=True).distinct()


class Opinion(models.Model):
    title = models.CharField(max_length=1023)
    content = models.TextField()
    url = models.URLField(max_length=400)
    institution = models.CharField(max_length=63, choices=((u'EU', 'european parliament'), (u'FR', 'assemblée nationale française')))
    _date = models.DateField(default=None, null=True, blank=True)
    _author = models.ForeignKey('Representative', default=None, null=True)

    def date(self):
        if self._date is None:
            _date = self.opinionrep_set.all()[0].date
            self._date = _date if _date else date(1, 1, 1)
            self.save()
        return self._date

    @reify
    def meps(self):
        return meps.models.MEP.objects.filter(opinionrep__opinion=self)

    def mps(self):
        return mps.models.MP.objects.filter(opinionrep__opinion=self)

    def authors(self):
        if self.institution == "FR":
            return self.mps()
        return self.meps()

    def author(self):
        if self._author is None:
            self._author = self.authors()[0]
            self.save()
        return self._author

    def get_absolute_url(self):
        if self.institution == "FR":
            return reverse("mps:index_by_opinions", args=[self.id])
        return reverse("meps:index_by_opinions", args=[self.id])

    @classmethod
    def with_meps_count(cls):
        return cls.objects.distinct().filter(institution="EU", opinionrep__representative__mep__active=True).annotate(authors_count=Count('opinionrep__representative__mep', distinct=True))

    @classmethod
    def with_mps_count(cls):
        return cls.objects.distinct().filter(institution="FR", opinionrep__representative__mp__active=True).annotate(authors_count=Count('opinionrep__representative__mp', distinct=True))

    @property
    def _q_objects(self):
        return Q(), Q()

    def __unicode__(self):
        return self.title


CURRENT_MAGIC_VAL=date(9999, 12, 31)

class TimePeriodQueryset(models.query.QuerySet):
    def newer_first(self):
        return self.order_by('-end', '-begin')

    def only_current(self):
        return self.filter(end=CURRENT_MAGIC_VAL)

    def only_old(self):
        return self.filter(end__lt=CURRENT_MAGIC_VAL)

    def at_date(self, _date):
        return self.filter(begin__lt=_date, end__gt=_date)[0]


class TimePeriodManager(models.Manager):
    use_for_related_fields = True

    def newer_first(self):
        return self.get_query_set().newer_first()

    def only_current(self):
        return self.get_query_set().only_current()

    def only_old(self):
        return self.get_query_set().only_old()

    def at_date(self, _date):
        return self.get_query_set().at_date(_date)

    def get_query_set(self):
        return TimePeriodQueryset(self.model)


class TimePeriod(models.Model):
    """
    Helper base class used on M2M intermediary models representing a
    relationship between a Representative and a Role (Group/Delegation/etc.)
    during a certain period in time.
    """
    class Meta:
        abstract = True

    objects = TimePeriodManager()

    begin = models.DateField(null=True)
    end = models.DateField(null=True)

    def is_current(self):
        if self.end == CURRENT_MAGIC_VAL:
            return True
        else:
            return False

    def is_past(self):
        if self.end < date.today():
            return True
        else:
            return False


class Representative(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=2, choices=((u'M', u'Male'), (u'F', u'Female')), null=True)
    picture = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField(null=True)
    birth_place = models.CharField(max_length=255)
    local_party = models.ManyToManyField(Party, through='PartyRepresentative')
    opinions = models.ManyToManyField(Opinion, through='OpinionREP')
    achievements = models.ManyToManyField('categories.Category')

    def __unicode__(self):
        if self.first_name and self.last_name:
            return u'%s %s' % (self.first_name, self.last_name.upper())
        elif self.full_name:
            return self.full_name
        else:
            return self.first_name or self.last_name
    content = __unicode__

    class Meta:
        ordering = ['last_name']

    @reify
    def emails(self):
        key = 'emails_%s' % self.id
        value = cache.get(key)
        if not value:
            value = [e.email for e in self.email_set.all()]
            cache.set(key, value, settings.SNIPPETS_CACHE_DELAY)
        return value

    @snippet(template='meps/snippets/group.html')
    def group_tag(self):
        return dict(group=self.group)


class PartyRepresentative(models.Model):
    representative = models.ForeignKey(Representative)
    party = models.ForeignKey(Party)
    role = models.CharField(max_length=255, null=True)
    current = models.BooleanField()
    # well maybe need those one day
    #begin = models.DateField()
    #end = models.DateField()


class Email(models.Model):
    email = models.EmailField()
    representative = models.ForeignKey(Representative)

    def __unicode__(self):
        return self.email


class CV(models.Model):
    title = models.TextField()
    representative = models.ForeignKey(Representative)

    def __unicode__(self):
        return self.title


class WebSite(models.Model):
    url = models.URLField()
    representative = models.ForeignKey(Representative)

    def __unicode__(self):
        return self.url or u'-'


class OpinionREP(models.Model):
    representative = models.ForeignKey(Representative)
    opinion = models.ForeignKey(Opinion)
    date = models.DateField()

    def __unicode__(self):
        return u"%s: %s" % (self.representative, self.opinion)
