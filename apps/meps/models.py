from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.name)

    @property
    def count(self):
        return len(self.meps)

    @property
    def meps(self):
        return self.mep_set.filter(active=True)

class Party(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    @property
    def count(self):
        return len(self.meps)

    @property
    def meps(self):
        return self.mep_set.filter(active=True)


class Group(models.Model):
    abbreviation = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return u"%s - %s" % (self.abbreviation, self.name)

    @property
    def count(self):
        return len(self.meps)

    @property
    def meps(self):
        return self.mep_set.filter(active=True)


class Deleguation(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    @property
    def count(self):
        return len(self.meps)

    @property
    def meps(self):
        return self.mep_set.filter(active=True)


class Committe(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return u"%s: %s" % (self.abbreviation, self.name)

    @property
    def count(self):
        return len(self.meps)

    @property
    def meps(self):
        return self.mep_set.filter(active=True)


class Opinion(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.CharField(max_length=255, unique=True)
    url = models.URLField()

    def __unicode__(self):
        return self.title

class MEP(models.Model):
    active = models.BooleanField()
    key_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=2, choices=((u'M', u'Male'), (u'F', u'Female')))
    picture = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=255)
    ep_id = models.IntegerField()
    ep_opinions = models.URLField()
    ep_debates = models.URLField()
    ep_questions = models.URLField()
    ep_declarations = models.URLField()
    ep_reports = models.URLField()
    ep_motions = models.URLField()
    ep_webpage = models.URLField()
    bxl_building_name = models.CharField(max_length=255)
    bxl_building_abbreviation = models.CharField(max_length=255)
    bxl_office = models.CharField(max_length=255)
    bxl_fax = models.CharField(max_length=255)
    bxl_phone1 = models.CharField(max_length=255)
    bxl_phone2 = models.CharField(max_length=255)
    bxl_street = models.CharField(max_length=255)
    bxl_postcode = models.CharField(max_length=255)
    stg_building_name = models.CharField(max_length=255)
    stg_building_abbreviation = models.CharField(max_length=255)
    stg_office = models.CharField(max_length=255)
    stg_fax = models.CharField(max_length=255)
    stg_phone1 = models.CharField(max_length=255)
    stg_phone2 = models.CharField(max_length=255)
    stg_street = models.CharField(max_length=255)
    stg_postcode = models.CharField(max_length=255)
    party = models.ForeignKey(Party)
    group = models.ForeignKey(Group)
    group_role = models.CharField(max_length=63)
    country = models.ForeignKey(Country)
    deleguations = models.ManyToManyField(Deleguation, through='DeleguationRole')
    opinions = models.ManyToManyField(Opinion, through='OpinionMEP')
    committes = models.ManyToManyField(Committe, through='CommitteRole')

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ['last_name']

class Email(models.Model):
    email = models.EmailField()
    mep = models.ForeignKey(MEP)

    def __unicode__(self):
        return self.email

class CV(models.Model):
    title = models.CharField(max_length=255)
    mep = models.ForeignKey(MEP)

    def __unicode__(self):
        return self.title

class WebSite(models.Model):
    url = models.URLField()
    mep = models.ForeignKey(MEP)

    def __unicode__(self):
        return self.url

class DeleguationRole(models.Model):
    mep = models.ForeignKey(MEP)
    deleguation = models.ForeignKey(Deleguation)
    role = models.CharField(max_length=255)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)

    def __unicode__(self):
        return u"%s : %s" % (self.mep.full_name, self.deleguation)

class CommitteRole(models.Model):
    mep = models.ForeignKey(MEP)
    committe = models.ForeignKey(Committe)
    role = models.CharField(max_length=255)
    begin = models.DateField(null=True)
    end = models.DateField(null=True)

    def __unicode__(self):
        return u"%s : %s" % (self.committe.abbreviation, self.mep.full_name)

class OpinionMEP(models.Model):
    mep = models.ForeignKey(MEP)
    opinion = models.ForeignKey(Opinion)
    date = models.DateField()

    def __unicode__(self):
        return u"%s : %s" % (self.opinion, self.mep)
