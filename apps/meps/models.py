from django.db import models

from reps.models import Representative

class MepsContainerManager(models.Manager):
    """ Manager for models to which the MEP model has a foreign key"""
    def with_counts(self):
        """ Return the models with a count property, with the count of active meps """
        return self.get_query_set().filter(mep__active=True).annotate(count=models.Count('mep'))


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=30, unique=True)

    objects = MepsContainerManager()

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.name)

    @property
    def meps(self):
        return self.mep_set.filter(active=True)


class Group(models.Model):
    abbreviation = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    objects = MepsContainerManager()

    def __unicode__(self):
        return u"%s - %s" % (self.abbreviation, self.name)

    @property
    def meps(self):
        return self.mep_set.filter(active=True)


class Deleguation(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = MepsContainerManager()

    def __unicode__(self):
        return self.name

    @property
    def meps(self):
        return self.mep_set.filter(active=True)


class Committee(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=30, unique=True)

    objects = MepsContainerManager()

    def __unicode__(self):
        return u"%s: %s" % (self.abbreviation, self.name)

    @property
    def meps(self):
        return self.mep_set.filter(active=True)


class Building(models.Model):
    """ A building of the European Parliament"""
    name = models.CharField(max_length=255)
    id = models.CharField('Abbreviation', max_length=255, primary_key=True)
    street = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)

class MEP(Representative):
    active = models.BooleanField()
    ep_id = models.IntegerField()
    ep_opinions = models.URLField()
    ep_debates = models.URLField()
    ep_questions = models.URLField()
    ep_declarations = models.URLField()
    ep_reports = models.URLField()
    ep_motions = models.URLField()
    ep_webpage = models.URLField()
    bxl_building = models.ForeignKey(Building)
    bxl_office = models.CharField(max_length=255)
    bxl_fax = models.CharField(max_length=255)
    bxl_phone1 = models.CharField(max_length=255)
    bxl_phone2 = models.CharField(max_length=255)
    stg_building = models.ForeignKey(Building)
    stg_office = models.CharField(max_length=255)
    stg_fax = models.CharField(max_length=255)
    stg_phone1 = models.CharField(max_length=255)
    stg_phone2 = models.CharField(max_length=255)
    group = models.ForeignKey(Group)
    group_role = models.CharField(max_length=63)
    country = models.ForeignKey(Country)
    deleguations = models.ManyToManyField(Deleguation, through='DeleguationRole')
    committees = models.ManyToManyField(Committee, through='CommitteeRole')

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ['last_name']

class DeleguationRole(models.Model):
    mep = models.ForeignKey(MEP)
    deleguation = models.ForeignKey(Deleguation)
    role = models.CharField(max_length=255)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)

    def __unicode__(self):
        return u"%s : %s" % (self.mep.full_name, self.deleguation)

class CommitteeRole(models.Model):
    mep = models.ForeignKey(MEP)
    committe = models.ForeignKey(Committee)
    role = models.CharField(max_length=255)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)

    def __unicode__(self):
        return u"%s : %s" % (self.committe.abbreviation, self.mep.full_name)

