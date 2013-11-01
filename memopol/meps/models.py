from datetime import date
from django.db import models
from django.db.models import Count, Q
from django.contrib.comments.moderation import CommentModerator, moderator
from django.core.urlresolvers import reverse
from snippets import snippet

from memopol.base.utils import reify, color
from memopol.reps.models import Representative, Party, TimePeriod, CURRENT_MAGIC_VAL


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.name)

    @property
    def meps(self):
        return self.mep_set.filter(active=True).distinct()
        #return self.mep_set.filter(active=True, countrymep__end=date(9999, 12, 31)).distinct()

    def meps_on_date(self, date):
        return self.mep_set.filter(groupmep__end__gte=date, groupmep__begin__lte=date).distinct()

    @classmethod
    def with_meps_count(cls):
        return cls.objects.distinct().filter(countrymep__mep__active=True).annotate(meps_count=Count('countrymep__mep', distinct=True))

    @property
    def _q_objects(self):
        return Q(mep__countrymep__country=self), Q(representative__mep__countrymep__country=self)

    class Meta:
        ordering = ["code"]


class LocalParty(Party):
    country = models.ForeignKey(Country, null=True)

    @property
    def _q_objects(self):
        return Q(mep__partyrepresentative__party=self), Q(representative__partyrepresentative__party=self)

    @classmethod
    def with_meps_count(cls):
        return cls.objects.distinct().filter(partyrepresentative__representative__mep__active=True).annotate(meps_count=Count('partyrepresentative__representative__mep', distinct=True))


class Group(models.Model):
    abbreviation = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return u"%s - %s" % (self.abbreviation, self.name)
    content = __unicode__

    def get_absolute_url(self):
        return reverse('meps:index_by_group', args=(self.abbreviation,))

    @property
    def meps(self):
        return self.mep_set.filter(active=True).distinct()
        #return self.mep_set.filter(active=True, groupmep__end=date(9999, 12, 31)).distinct()

    def meps_on_date(self, date):
        return self.mep_set.filter(groupmep__end__gte=date, groupmep__begin__lte=date).distinct()

    @property
    def _q_objects(self):
        return Q(mep__groupmep__group=self), Q(representative__mep__groupmep__group=self)

    @classmethod
    def ordered_by_meps_count(cls):
        return (cls.objects.distinct().filter(groupmep__mep__active=True, groupmep__end=CURRENT_MAGIC_VAL)
                           .annotate(meps_count=Count('groupmep__mep', distinct=True)).order_by('-meps_count'))


class Delegation(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name
    content = __unicode__

    def get_absolute_url(self):
        return reverse('meps:index_by_delegation', args=(self.id,))

    @property
    def meps(self):
        return self.mep_set.filter(active=True).distinct()
        #return self.mep_set.filter(active=True, delegationrole__end=date(9999, 12, 31)).distinct()

    @property
    def _q_objects(self):
        return Q(mep__delegationrole__delegation=self), Q(representative__mep__delegationrole__delegation=self)

    @classmethod
    def with_meps_count(cls):
        return (cls.objects.distinct().filter(delegationrole__mep__active=True, delegationrole__end=CURRENT_MAGIC_VAL)
                           .annotate(meps_count=Count('delegationrole__mep', distinct=True)))


class Committee(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return u"%s: %s" % (self.abbreviation, self.name)
    content = __unicode__

    def get_absolute_url(self):
        return reverse('meps:index_by_committee', args=(self.abbreviation,))

    @property
    def meps(self):
        return self.mep_set.filter(active=True).distinct()

    @property
    def _q_objects(self):
        return Q(mep__committeerole__committee=self), Q(representative__mep__committeerole__committee=self)

    @classmethod
    def ordered_by_meps_count(cls):
        return (cls.objects.distinct().filter(committeerole__mep__active=True, committeerole__end=CURRENT_MAGIC_VAL)
                           .annotate(meps_count=Count('committeerole__mep', distinct=True)).order_by('-meps_count'))


class Building(models.Model):
    """ A building of the European Parliament"""
    name = models.CharField(max_length=255)
    id = models.CharField('Abbreviation', max_length=255, primary_key=True)
    street = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)

    class Meta:
        ordering = ('postcode', 'pk',)

    @reify
    def _town(self):
        return "bxl" if self.postcode == "1047" else "stg"

    @reify
    def floors(self):
        floors = []
        def add(x):
            if getattr(x, "%s_floor" % self._town) not in floors:
                floors.append(getattr(x, "%s_floor" % self._town))
        map(add, self.meps.order_by("%s_floor" % self._town))
        return floors

    @reify
    def meps(self):
        return getattr(self, "%s_building" % self._town).filter(active=True)

    def __unicode__(self):
        return u"%s - %s - %s - %s" % (self.id, self.name, self.street, self.postcode)


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name
    content = __unicode__

    def get_absolute_url(self):
        return reverse('meps:index_by_organization', args=(self.id,))

    @property
    def meps(self):
        return self.mep_set.filter(active=True).distinct()
        #return self.mep_set.filter(active=True, organizationmep__end=date(9999, 12, 31)).distinct()

    @property
    def _q_objects(self):
        return Q(mep__organizationmep__organization=self), Q(representative__mep__organizationmep__organization=self)

    @classmethod
    def with_meps_count(cls):
        return cls.objects.distinct().filter(organizationmep__mep__active=True).annotate(meps_count=Count('organizationmep__mep', distinct=True))


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
    bxl_building = models.ForeignKey(Building, related_name="bxl_building", null=True)
    bxl_floor = models.CharField(max_length=255, null=True)
    bxl_office_number = models.CharField(max_length=255, null=True)
    bxl_fax = models.CharField(max_length=255, null=True)
    bxl_phone1 = models.CharField(max_length=255, null=True)
    bxl_phone2 = models.CharField(max_length=255, null=True)
    stg_building = models.ForeignKey(Building, related_name="stg_building", null=True)
    stg_floor = models.CharField(max_length=255, null=True)
    stg_office_number = models.CharField(max_length=255, null=True)
    stg_fax = models.CharField(max_length=255, null=True)
    stg_phone1 = models.CharField(max_length=255, null=True)
    stg_phone2 = models.CharField(max_length=255, null=True)
    groups = models.ManyToManyField(Group, through='GroupMEP')
    countries = models.ManyToManyField(Country, through='CountryMEP')
    delegations = models.ManyToManyField(Delegation, through='DelegationRole')
    committees = models.ManyToManyField(Committee, through='CommitteeRole')
    organizations = models.ManyToManyField(Organization, through='OrganizationMEP')
    position = models.IntegerField(default=None, null=True)
    total_score = models.FloatField(default=None, null=True)

    def age(self):
        if date.today().month > self.birth_date.month:
            return date.today().year - self.birth_date.year
        elif date.today().month == self.birth_date.month and date.today().day > self.birth_date.day:
            return date.today().year - self.birth_date.year
        else:
            return date.today().year - self.birth_date.year + 1

    @reify
    def get_ep_webpage(self):
        if self.active and self.ep_webpage:
            return self.ep_webpage
        return None

    def get_absolute_url(self):
        return reverse('meps:mep', args=(self.id,))

    @reify
    def bxl_office(self):
        return self.bxl_floor + self.bxl_office_number

    @reify
    def stg_office(self):
        return self.stg_floor + self.stg_office_number

    @reify
    def groups_mep(self):
        return self.groupmep_set.select_related('group')

    @reify
    def group(self):
        try:
            return self.groups_mep.latest('end').group
        except GroupMEP.DoesNotExist:
            return None

    @reify
    def country(self):
        return self.countries_mep.latest('end').country

    @reify
    def party(self):
        return self.countries_mep.latest('end').party

    @reify
    def countries_mep(self):
        return self.countrymep_set.select_related('country', 'party')

    @reify
    def delegations_roles(self):
        return self.delegationrole_set.select_related('delegation')

    @reify
    def committees_roles(self):
        return self.committeerole_set.select_related('committee')

    @reify
    def organizations_mep(self):
        return self.organizationmep_set.select_related('organization')

    @reify
    def assistants_mep(self):
        return self.assistantmep_set.select_related('assistant')

    @property
    def score_color(self):
        return "rgb(%s, %s, %s)" % color(self.total_score)

    @snippet(template='meps/snippets/country.html')
    def country_tag(self):
        return dict(country=self.country)

    @snippet(template='meps/snippets/party.html')
    def party_tag(self):
        return dict(party=self.party)

    @reify
    def important_posts(self):
        all_roles = list(self.organizations_mep.only_current())
        for i in (self.groups_mep.only_current().exclude(role="").exclude(role="Member").exclude(role="Substitute"),
                  self.committees_roles.only_current()):
            roles = i.filter(mep=self)
            if roles:
                all_roles += list(roles)
        return all_roles

    class Meta:
        ordering = ['last_name']


class GroupMEP(TimePeriod):
    mep = models.ForeignKey(MEP)
    group = models.ForeignKey(Group)
    role = models.CharField(max_length=255)

    @reify
    def instance(self):
        return self.group


class DelegationRole(TimePeriod):
    mep = models.ForeignKey(MEP)
    delegation = models.ForeignKey(Delegation)
    role = models.CharField(max_length=255)

    @reify
    def instance(self):
        return self.delegation

    def __unicode__(self):
        return u"%s : %s" % (self.mep.full_name, self.delegation)


class CommitteeRole(TimePeriod):
    mep = models.ForeignKey(MEP)
    committee = models.ForeignKey(Committee)
    role = models.CharField(max_length=255)

    @reify
    def instance(self):
        return self.committee

    def __unicode__(self):
        return u"%s : %s" % (self.committee.abbreviation, self.mep.full_name)


class PostalAddress(models.Model):
    addr = models.CharField(max_length=255)
    mep = models.ForeignKey(MEP)


class CountryMEP(TimePeriod):
    mep = models.ForeignKey(MEP)
    country = models.ForeignKey(Country)
    party = models.ForeignKey(LocalParty)


class OrganizationMEP(TimePeriod):
    mep = models.ForeignKey(MEP)
    organization = models.ForeignKey(Organization)
    role = models.CharField(max_length=255)

    @reify
    def instance(self):
        return self.organization


class MepModerator(CommentModerator):
    email_notification = True
    moderate_after = 0
    def moderate(self, comment, content_object, request):
        return True


moderator.register(MEP, MepModerator)


class Assistant(models.Model):
    full_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.full_name

class AssistantMEP(models.Model):
    mep = models.ForeignKey(MEP)
    assistant = models.ForeignKey(Assistant)
    type = models.CharField(max_length=255)
    # active = models.BooleanField()
