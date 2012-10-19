#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import urllib
from os.path import join
from time import time
import logging
import datetime
from json import dumps

from django.conf import settings
from django.views.generic import DetailView, ListView
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from memopol2.utils import check_dir, send_file, get_content_cache

from models import LocalParty, Building, MEP, CountryMEP, GroupMEP, Committee, Group, Country, Organization, Delegation
from reps.models import Email
from votes.models import Score, Vote

UE_IMAGE_URL = u"http://www.europarl.europa.eu/mepphoto/%s.jpg"

logger = logging.getLogger(__name__)


generic_operations = {
    "active": lambda queryset, argument: queryset.filter(active=argument),
    "country": lambda queryset, argument: queryset.filter(countrymep__country__code=argument.upper()),
    "group": lambda queryset, argument: queryset.filter(groupmep__group__abbreviation=argument),
    "committee": lambda queryset, argument: queryset.filter(committeerole__committee__abbreviation=argument.upper()),
    "delegation": lambda queryset, argument: queryset.filter(delegationrole__delegation__id=argument),
    "score_min": lambda queryset, argument: queryset.filter(total_score__gt=argument),
    "score_max": lambda queryset, argument: queryset.filter(total_score__lt=argument),
    "last_name": lambda queryset, argument: queryset.filter(last_name=argument.upper()),
    "bxl_floor": lambda queryset, argument: queryset.filter(bxl_floor=argument.upper()),
    "bxl_building": lambda queryset, argument: queryset.filter(bxl_building=argument.upper()),
    "stg_floor": lambda queryset, argument: queryset.filter(stg_floor=argument.upper()),
    "stg_building": lambda queryset, argument: queryset.filter(stg_building=argument.upper()),
    "organization": lambda queryset, argument: queryset.filter(organizationmep__organization__id=argument),
}

convert_arguments_table = {
    "true": True,
    "false": False,
}



def convert_argument(argument):
    return convert_arguments_table.get(argument, argument)


def generic(request):
    GET_arguments_in_generic_operations = filter(lambda x: x in generic_operations.keys(), request.GET)

    queryset = MEP.objects.all()
    for i in GET_arguments_in_generic_operations:
        queryset = generic_operations[i](queryset, convert_argument(request.GET[i]))

    queryset = optimise_mep_query(queryset.distinct())

    return render(request, "meps/generic.html", {"meps": queryset, "fields": generic_operations.keys()})


filters = {
    "active": lambda: [["true", "true"], ["false", "false"]],
    "country": lambda: [[x.code, x.name] for x in Country.objects.all()],
    "group": lambda: [[x.abbreviation, "(%s) " % x.abbreviation + x.name] for x in Group.objects.all()],
    "committee": lambda: [[x.abbreviation, "(%s) " % x.abbreviation + x.name] for x in Committee.objects.all()],
    "delegation": lambda: [[x.id, x.name[:85] + ("..." if len(x.name) > 84 else "")] for x in Delegation.objects.all()],
    "bxl_floor": lambda: [[x, x] for x in sorted(filter(None, set(map(lambda x: x.bxl_floor, MEP.objects.all()))))],
    "bxl_building": lambda: [[x.id, "(%s) %s" % (x.id, x.name)] for x in filter(lambda x: x._town == "bxl", Building.objects.all())],
    "stg_floor": lambda: [[x, x] for x in sorted(filter(None, set(map(lambda x: x.stg_floor, MEP.objects.all()))))],
    "stg_building": lambda: [[x.id, "(%s) %s" % (x.id, x.name)] for x in filter(lambda x: x._town == "stg", Building.objects.all())],
    "organization": lambda: [[x.id, x.name] for x in Organization.objects.all()],
}


def get_filter(request, name):
    if filters.get(name):
        return HttpResponse(dumps(filters[name]()))
    else:
        return HttpResponse('')


def get_mep_picture(request, ep_id):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'meps', u"%s.jpg" % ep_id)
    cache = get_content_cache(request, filename, 'image/jpeg')
    if cache:
        return cache
    check_dir(filename)
    urllib.urlretrieve(UE_IMAGE_URL % ep_id, filename)
    return send_file(request, filename, content_type='image/jpeg')


def render_to_csv(view, context, **response_kwargs):
    params = view.request.GET
    response = HttpResponse(mimetype='text/csv')
    name = view.request.path.strip('/').replace('/', '_')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % name

    header = [
            'name',
            'gender',
            'score',
            'emails',
            'country',
            'group',
            'bxl building id',
            'bxl building name',
            'bxl floor',
            'bxl office number',
            'bxl fax',
            'bxl phone1',
            'bxl phone2',
            'stg building id',
            'stg building name',
            'stg floor',
            'stg office number',
            'stg fax',
            'stg phone1',
            'stg phone2',
    ]

    committees = sorted([c.abbreviation for c in Committee.objects.all()])

    header += committees

    meps = []

    max_score = int(params.get('max_score', 100))
    min_score = int(params.get('min_score', -100))

    if 'object' in context:
        obj = context['object']
        meps = getattr(obj, 'meps', [])

    if hasattr(meps, 'query'):
        # got a queryset
        meps = meps.select_related().distinct()
        if 'group' in params:
            meps = meps.filter(groups__abbreviation=params['group'])
        if 'country' in params:
            meps = meps.filter(countries__name=params['country'])

    writer = csv.writer(response, delimiter=';',
                                  quotechar='"',
                                  doublequote=True)
    writer.writerow(header)

    for mep in meps:

        # re-filter in case of non queryset objects
        if 'group' in params and \
            mep.group.abbreviation != params['group']:
            continue
        if 'country' in params and \
            params['country'] not in (mep.country.name,
                                      mep.country.code):
            continue
        if mep.total_score and\
               (mep.total_score < min_score or \
               mep.total_score > max_score):
            continue

        row = [
            unicode(mep),
            mep.gender,
            int(mep.total_score) if mep.total_score else '',
            u' - '.join(mep.emails),
            mep.country.name,
            mep.group.abbreviation,
            mep.bxl_building.id if mep.bxl_building else '',
            mep.bxl_building.name if mep.bxl_building else '',
            mep.bxl_floor,
            mep.bxl_office_number,
            mep.bxl_fax,
            mep.bxl_phone1,
            mep.bxl_phone2,
            mep.stg_building.id if mep.stg_building else '',
            mep.stg_building.name if mep.stg_building else '',
            mep.stg_floor,
            mep.stg_office_number,
            mep.stg_fax,
            mep.stg_phone1,
            mep.stg_phone2,
        ]
        str_row = []
        for v in row:
            if isinstance(v, unicode):
                v = v.encode('utf-8')
            str_row.append(v)

        mep_committees = {}
        # FIXME: this should use current_committees but it look like its broken
        # or no longer valid
        roles = mep.committeerole_set.all()
        for role in roles:
            abbr = role.committee.abbreviation
            mep_committees.setdefault(abbr, set([])).add(role.role)
        for c in committees:
            str_row.append(' - '.join(sorted(mep_committees.get(c, []))))

        assert len(str_row) == len(header)
        writer.writerow(str_row)

    return response


class BuildingDetailView(DetailView):
    context_object_name = "building"
    model = Building

    def get_context_data(self, *args, **kwargs):
        context = super(BuildingDetailView, self).get_context_data(**kwargs)
        context['meps'] = optimise_mep_query(MEP.objects.filter(active=True,
                                                                **{'%s_building' % self.object._town: self.object,
                                                                   '%s_floor' % self.object._town: self.kwargs["floor"]}),
                                             Q(mep__active=True, **{'mep__%s_building' % self.object._town: self.object,
                                                                    'mep__%s_floor' % self.object._town: self.kwargs["floor"]}),
                                               Q(representative__mep__active=True, **{'representative__mep__%s_building' % self.object._town: self.object,
                                                                                      'representative__mep__%s_floor' % self.object._town: self.kwargs["floor"]}))
        context['floor'] = self.kwargs['floor']
        return context


class MEPList(ListView):
    active=True
    context_object_name="mep"
    score_listing=False
    order_by='last_name'

    def get_queryset(self):
        if not self.queryset:
            return MEP.objects.filter(active=self.active).order_by(self.order_by)
        return self.queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MEPList, self).get_context_data(**kwargs)
        optimise_mep_query(context["object_list"], Q(mep__active=self.active), Q(representative__mep__active=self.active), score_listing=self.score_listing)
        context['score_listing'] = self.score_listing
        context['active'] = self.active
        return context

    def render_to_response(self, context, **response_kwargs):
        if 'csv' in self.request.GET:
            return render_to_csv(self, context, **response_kwargs)
        return super(MEPList, self).render_to_response(context,
                                                       **response_kwargs)


def optimise_mep_query(queryset, q_object=Q(), q_object_rep=Q(), score_listing=False, proposal_score=None, choice_on_recommendation=None):
    """
    The following piece of code could be remove once the prefetch_related()
    feature becomes available in Django ORM [1].
    Since Django cannot yet follow oneToMany and ManyToMany relations,
    we populate MEP objects manually in python. It does not hurt kittens
    and boosts performance, greatly.

    [1] https://docs.djangoproject.com/en/dev/topics/db/optimization/#use-queryset-select-related-and-prefetch-related
    """
    start = time()
    country_mep = {}
    for country in CountryMEP.objects.filter(q_object).select_related('mep', 'country').order_by('mep', 'end').all():
        country_mep[country.mep.id] = country.country
    group_mep = {}
    groupmep_mep = {}
    for group in GroupMEP.objects.filter(q_object).select_related('mep', 'group').order_by('mep', 'end').all():
        group_mep[group.mep.id] = group.group
        groupmep_mep[group.mep.id] = group
    emails_mep = {}
    for email in Email.objects.filter(q_object_rep).select_related('representative').all():
        emails_mep.setdefault(email.representative.id, []).append(email.email)

    if score_listing:
        scores_mep = {}
        for score in Score.objects.filter(q_object_rep).select_related('proposal', 'representative'):
            scores_mep.setdefault(score.representative.id, []).append(score)

    if proposal_score:
        proposal_score_mep = {}
        for score in proposal_score.score_set.select_related('representative'):
            proposal_score_mep[score.representative.id] = score

    if choice_on_recommendation:
        choice_mep = {}
        for vote in Vote.objects.filter(recommendation=choice_on_recommendation, representative__isnull=False).select_related('representative'):
            choice_mep[vote.representative.id] = vote.choice

    # Overwrite MEP attributes
    for mep in queryset:
        mep.country = country_mep.get(mep.id)
        mep.group = group_mep.get(mep.id)
        mep.groupmep = groupmep_mep.get(mep.id)
        mep.emails = emails_mep.get(mep.id)
        if score_listing:
            mep.scores = scores_mep.get(mep.id)
        if proposal_score:
            mep.score = proposal_score_mep[mep.id]
        if choice_on_recommendation:
            mep.choice = choice_mep[mep.id]
    logger.debug("MEPList relationships took %.2fsec to build." % (time() - start))
    return queryset


class MEPView(DetailView):
    queryset=MEP.objects.all().select_related('bxl_building', 'stg_building').prefetch_related('cv_set')
    context_object_name="mep"

    def get_context_data(self, *args, **kwargs):
        context = super(MEPView, self).get_context_data(**kwargs)
        context['now'] = datetime.date.today()
        context['mep'].delegationroles = context['mep'].delegationrole_set.all().select_related('delegation')
        context['mep'].committeeroles = context['mep'].committeerole_set.all().select_related('committee')
        context['mep'].opinionreps = context['mep'].opinionrep_set.all().select_related('opinion')
        context['mep'].scores = context['mep'].score_set.all().select_related('proposal')
        return context


class MEPsFromView(DetailView):
    template_name='meps/container_detail.html'
    hidden_fields = []
    named_header='meps/named_header.html'
    organization_role=False
    group_role=False
    committee_role=False
    delegation_role=False

    def get_context_data(self, *args, **kwargs):
        context = super(MEPsFromView, self).get_context_data(**kwargs)
        context['header_template'] = self.named_header
        context['hidden_fields'] = self.hidden_fields
        context['organization_role'] = self.organization_role
        context['group_role'] = self.group_role
        context['committee_role'] = self.committee_role
        context['delegation_role'] = self.delegation_role
        context['meps'] = optimise_mep_query(context['object'].meps, *context['object']._q_objects)
        return context

    def render_to_response(self, context, **response_kwargs):
        if 'csv' in self.request.GET:
            return render_to_csv(self, context, **response_kwargs)
        return super(MEPsFromView, self).render_to_response(context,
                                                       **response_kwargs)

class PartyView(MEPsFromView):
    model=LocalParty
    hidden_fields=['party']

    def render_to_response(self, context):
        if self.kwargs['slugified_name'] != slugify(self.object.name):
            return HttpResponseRedirect(reverse('meps:index_by_party', args=[self.object.id, slugify(self.object.name)]))
        return MEPsFromView.render_to_response(self, context)
