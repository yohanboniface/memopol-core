from datetime import date
from django.db import models
from django.contrib.comments.moderation import CommentModerator, moderator
from memopol2.utils import snippet

from reps.models import Representative, Party

class MepsContainerManager(models.Manager):
    """ Manager for models to which the MEP model has a foreign key"""
    def with_counts(self):
        """ Return the models with a count property, with the count of active meps """
        # FIXME don't work as expected now, show historical count instead of current count
        return self.get_query_set().filter(mep__active=True).annotate(count=models.Count('mep'))


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=30, unique=True)

    objects = MepsContainerManager()

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.name)

    @property
    def meps(self):
        return self.mep_set.filter(active=True, countrymep__end=date(9999, 12, 31)).distinct()


class Group(models.Model):
    abbreviation = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    objects = MepsContainerManager()

    def __unicode__(self):
        return u"%s - %s" % (self.abbreviation, self.name)

    @property
    def meps(self):
        return self.mep_set.filter(active=True, groupmep__end=date(9999, 12, 31)).distinct()


class Delegation(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = MepsContainerManager()

    def __unicode__(self):
        return self.name

    @property
    def meps(self):
        return self.mep_set.filter(active=True, delegationrole__end=date(9999, 12, 31)).distinct()


class Committee(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=30, unique=True)

    objects = MepsContainerManager()

    def __unicode__(self):
        return u"%s: %s" % (self.abbreviation, self.name)

    @property
    def meps(self):
        return self.mep_set.filter(active=True, committeerole__end=date(9999, 12, 31)).distinct()


class Building(models.Model):
    """ A building of the European Parliament"""
    name = models.CharField(max_length=255)
    id = models.CharField('Abbreviation', max_length=255, primary_key=True)
    street = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    @property
    def meps(self):
        return self.mep_set.filter(active=True, organizationmep__end=date(9999, 12, 31)).distinct()



class MEP(Representative):
    active = models.BooleanField()
    ep_id = models.IntegerField(unique=True)
    ep_opinions = models.URLField()
    ep_debates = models.URLField()
    ep_questions = models.URLField()
    ep_declarations = models.URLField()
    ep_reports = models.URLField()
    ep_motions = models.URLField()
    ep_webpage = models.URLField()
    bxl_building = models.ForeignKey(Building, related_name="bxl_building")
    bxl_office = models.CharField(max_length=255)
    bxl_fax = models.CharField(max_length=255)
    bxl_phone1 = models.CharField(max_length=255)
    bxl_phone2 = models.CharField(max_length=255)
    stg_building = models.ForeignKey(Building, related_name="stg_building")
    stg_office = models.CharField(max_length=255)
    stg_fax = models.CharField(max_length=255)
    stg_phone1 = models.CharField(max_length=255)
    stg_phone2 = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, through='GroupMEP')
    countries = models.ManyToManyField(Country, through='CountryMEP')
    delegations = models.ManyToManyField(Delegation, through='DelegationRole')
    committees = models.ManyToManyField(Committee, through='CommitteeRole')
    organizations = models.ManyToManyField(Organization, through='OrganizationMEP')

    def __unicode__(self):
        if self.full_name:
            return self.full_name
        return u'%s %s' (self.first_name, self.last_name)

    @property
    def group(self):
        return self.groupmep_set.latest('end').group

    @property
    def country(self):
        return self.countrymep_set.latest('end').country

    def current_delegations(self):
        return self.delegationrole_set.filter(end=date(9999, 12, 31))

    group_tag = snippet('group')
    country_tag = snippet('country')
    party_tag = snippet('party')

    class Meta:
        ordering = ['last_name']


class GroupMEP(models.Model):
    mep = models.ForeignKey(MEP)
    group = models.ForeignKey(Group)
    role = models.CharField(max_length=255)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)


class DelegationRole(models.Model):
    mep = models.ForeignKey(MEP)
    delegation = models.ForeignKey(Delegation)
    role = models.CharField(max_length=255)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)

    def __unicode__(self):
        return u"%s : %s" % (self.mep.full_name, self.delegation)


class CommitteeRole(models.Model):
    mep = models.ForeignKey(MEP)
    committee = models.ForeignKey(Committee)
    role = models.CharField(max_length=255)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)

    def __unicode__(self):
        return u"%s : %s" % (self.committee.abbreviation, self.mep.full_name)


class PostalAddress(models.Model):
    addr = models.CharField(max_length=255)
    mep = models.ForeignKey(MEP)


class CountryMEP(models.Model):
    mep = models.ForeignKey(MEP)
    country = models.ForeignKey(Country)
    party = models.ForeignKey(Party)
    begin = models.DateField()
    end = models.DateField()


class OrganizationMEP(models.Model):
    mep = models.ForeignKey(MEP)
    organization = models.ForeignKey(Organization)
    role = models.CharField(max_length=255)
    begin = models.DateField()
    end = models.DateField()


class MepModerator(CommentModerator):
    email_notification = True
    moderate_after        = 0
    def moderate(self, comment, content_object, request):
        return True


moderator.register(MEP, MepModerator)

