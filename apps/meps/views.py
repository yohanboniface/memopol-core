import time
from datetime import datetime

import simplejson

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib.admin.views.decorators import staff_member_required

from meps.models import MEP

def score_to_color(score):
    """
    map a score between 0 and 100 to a red-green colorspace
    """
    red = 255 - score
    green = score * 2.55
    return "rgb(%d, %d, 0)" % (red, green)

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

def mep(request, mep_id):
    mep = get_object_or_404(MEP, key_name=mep_id)

    return direct_to_template(request, 'meps/mep.html', {'mep': mep})

def mep_json(request, mep_id):
    mep_ = MEP.get(mep_id)
    jsonstr = simplejson.dumps(dict(mep_), indent=4, use_decimal=True)
    return HttpResponse(jsonstr)

def mep_raw(request, mep_id):
    mep_ = MEP.get(mep_id)
    jsonstr = simplejson.dumps(dict(mep_), indent=4, use_decimal=True)
    context = {
        'mep_id': mep_id,
        'mep': mep_,
        'jsonstr': jsonstr,
    }
    return direct_to_template(request, 'meps/mep_raw.html', context)

def mep_addposition(request, mep_id):
    if not request.is_ajax():
        return HttpResponseServerError()
    results = {'success':False}
    # make sure the mep exists
    mep_ = MEP.view('meps/by_id', key=mep_id).first()

    # For testing purpose: add the possibility to cause a failure in the js (if
    # in debug) to see what's would happened for the user
    try:
        text = request.GET.get(u'text', '')
        if settings.DEBUG:
            if 'slow' in text:
                time.sleep(10)
            if 'fail' in text:
                raise Exception("Simulated failure ! (input contains 'fail' and DEBUG is on)")
        pos = Position(mep_id=mep_id, content=text)
        pos.submitter_username = request.user.username
        pos.submitter_ip = request.META["REMOTE_ADDR"]
        pos.submit_datetime = datetime.today()
        pos.moderated = False
        pos.visible = False
        pos.save()
        results = {'success':True}
    except:
        pass
    return HttpResponse(simplejson.dumps(results), mimetype='application/json')

@staff_member_required
def moderation(request):
    positions = Position.objects.filter(moderated=False)
    context = {
        'positions': positions,
    }
    return direct_to_template(request, 'meps/moderation.html', context)

@staff_member_required
def moderation_get_unmoderated_positions(request):
    if not request.is_ajax():
        return HttpResponseServerError()

    last_id = request.GET[u'last_id']
    positions =  Position.objects.filter(moderated=False, id__gt=last_id)
    return HttpResponse(serializers.serialize('json', positions), mimetype='application/json')

@staff_member_required
def moderation_moderate_positions(request):
    if not request.is_ajax():
        return HttpResponseServerError()
    results = {'success':False}
    position = get_object_or_404(Position, pk=int(request.GET[u'pos_id']))
    try:
        position.moderated = True
        position.visible = (request.GET[u'decision'] == "1")
        position.save()
        results = {'success':True}
    except:
        pass
    return HttpResponse(simplejson.dumps(results), mimetype='application/json')

