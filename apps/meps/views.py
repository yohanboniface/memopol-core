#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from os.path import join

from django.conf import settings
from django.views.generic import DetailView, ListView

from memopol2.utils import check_dir, send_file, get_content_cache

from models import Building, MEP

UE_IMAGE_URL = u"http://www.europarl.europa.eu/mepphoto/%s.jpg"

def get_mep_picture(request, ep_id):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'meps', u"%s.jpg" % ep_id)
    cache = get_content_cache(request, filename, 'image/jpeg')
    if cache:
        return cache
    check_dir(filename)
    urllib.urlretrieve(UE_IMAGE_URL % ep_id, filename)
    return send_file(request, filename, content_type='image/jpeg')

def autoTrophies(mep):
    mapping = { (u'Parlement europ\u00e9en',u'Pr\u00e9sident') : (12, 'President of EP', 'pep.jpg'),
                (u'Parlement europ\u00e9en',u'Vice-Pr\u00e9sident') : (11, 'VP of EP', 'vpep.jpg'),
                (u'Bureau du Parlement europ\u00e9en',u'Pr\u00e9sident') : (11,'President of EU Parlament Office', 'pepo.jpg'),
                (u'Bureau du Parlement europ\u00e9en',u'Vice-Pr\u00e9sident') : (10, 'VP of EU Parlament Office', 'vpepo.jpg'),
                (u'Bureau du Parlement europ\u00e9en',u'Membre') : (9, 'Member of EU Parlament Office', 'mepo.jpg'),
                (u'Conf\u00e9rence des pr\u00e9sidents', u'Pr\u00e9sident') : (11, "CoP President", 'pcop.jpg'),
                (u'Conf\u00e9rence des pr\u00e9sidents', u'Vice-pr\u00e9sident') : (9, "CoP VP", 'vpcop.jpg'),
                (u'Conf\u00e9rence des pr\u00e9sidents', u'Membre') : (8, "CoP Member", 'mcop.jpg'),
                (u'Conf\u00e9rence des pr\u00e9sidents des commissions', u'Pr\u00e9sident') : (7, "CoCP President", 'pcocp.jpg'),
                (u'Conf\u00e9rence des pr\u00e9sidents des commissions', u'Vice-pr\u00e9sident') : (6, "CoCP VP", 'vpcocp.jpg') ,
                (u'Conf\u00e9rence des pr\u00e9sidents des commissions', u'Membre') : (5, "CoCP Member", 'mcocp.jpg'),
                }
    res=[]
    for fn in mep.functions:
        try: # for Mr Lehnes record
            m=mapping.get((fn['label'],fn['role']))
        except TypeError:
            m=None
        if m:
            res.append(m)
            continue
        if fn.get('abbreviation'):
            if fn['role'].startswith(u'Pr\u00e9sident'): res.append((7, fn['abbreviation']+" President", 'presc.jpg'))
            elif fn['role'].startswith(u'Vice-pr\u00e9sident'): res.append((5,fn['abbreviation']+" VP", 'vpc.jpg'))
            elif fn['role'] == u'Membre': res.append( (2,fn['abbreviation']+" Member", 'mc.jpg'))
            elif fn['role'] == u'Membre suppl\u00e9ant': res.append((1, fn['abbreviation']+" Supplement", 'sc.jpg'))
    if mep.infos['group']['role'] in [u'Pr\u00e9sident', u'Copr\u00e9sident']:
        res.append((12, 'President of '+mep.infos['group']['abbreviation'], 'pg.jpg'))
    if mep.infos['group']['role'].startswith(u'Vice-pr\u00e9sident'):
        res.append((10, 'VP of '+mep.infos['group']['abbreviation'], 'vpg.jpg'))
    for op in mep.opinions:
        if op['url'] == 'http://www.laquadrature.net/wiki/Written_Declaration_12/2010_signatories_list':
            res.append((5, 'signed WD12', 'wd12.jpg'))
    return [(x[1], x[2]) for x in sorted(res, reverse=True)]


class BuildingDetailView(DetailView):
    context_object_name = "building"
    model = Building

    def get_context_data(self, *args, **kwargs):
        context = super(BuildingDetailView, self).get_context_data(**kwargs)
        context['meps'] = MEP.objects.filter(active=True,
                                             **{'%s_building' % self.object._town: self.object,
                                                '%s_floor' % self.object._town: self.kwargs["floor"]})
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
        context['score_listing'] = self.score_listing
        return context


class MEPView(DetailView):
    model = MEP
    context_object_name = "mep"


class MEPsFromView(DetailView):
    template_name='meps/container_detail.html'
    hidden_fields = []
    named_header='meps/named_header.html'
    organization_role=False
    group_role=False
    committee_role=False

    def get_context_data(self, *args, **kwargs):
        context = super(MEPsFromView, self).get_context_data(**kwargs)
        context['header_template'] = self.named_header
        context['hidden_fields'] = self.hidden_fields
        context['organization_role'] = self.organization_role
        context['group_role'] = self.group_role
        context['committee_role'] = self.committee_role
        return context
