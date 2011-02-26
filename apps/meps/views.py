import time
from datetime import datetime

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.core import serializers
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib.admin.views.decorators import staff_member_required

from meps.models import *

def index_names(request):
    meps_by_name = MEP.view('meps/by_name')
    context = {
        'meps': meps_by_name,
    }
    return direct_to_template(request, 'index.html', context)

def index_groups(request):

    groups = list(MEP.view('meps/groups', group=True))
    groups.sort(key=lambda group: group['value']['count'], reverse=True)

    context = {
        'groups': groups,
    }
    return direct_to_template(request, 'index.html', context)

def index_countries(request):

    countries = list(MEP.view('meps/countries', group=True))
    countries.sort(key=lambda group: group['value']['count'], reverse=True)

    context = {
        'countries': countries,
    }
    return direct_to_template(request, 'index.html', context)

def index_by_country(request, country_code):
    meps_by_country = MEP.view('meps/by_country', key=country_code)
    country_infos = MEP.view('meps/countries', key=country_code)

    context = {
        'meps': meps_by_country,
        'country': list(country_infos)[0]['value']['name'],
    }
    return direct_to_template(request, 'index.html', context)

def index_by_group(request, group):
    meps_by_group = MEP.view('meps/by_group', key=group)
    group_infos = MEP.view('meps/groups', key=group)
    context = {
        'meps': meps_by_group,
        'group': list(group_infos)[0]['value']['name'],
    }
    return direct_to_template(request, 'index.html', context)

def mep(request, mep_id):
    mep_ = MEP.view('meps/by_id', key=mep_id).first()
    positions = Position.objects.filter(mep_id=mep_id)
    score_list = mep_.scores
    print score_list
    print "XXX"
    score_list.sort(key = lambda k : k['value'])
    print score_list
    scores = [s['value'] for s in mep_.scores]
    
    context = {
        'mep_id': mep_id,
        'mep': mep_,
        'positions': positions,
        'visible_count': len([x for x in positions if x.visible]),
        'average': sum(scores)/len(scores) if len(scores) > 0 else "",
        'score_list' : score_list,
        'vote_colors' : ['#ff0000', '#dd0022', '#bb0044', '#dd0022', '#bb0044', '#990066', '#770088', '#5500aa', '#3300cc', '#1100ee', '#0000ff'],
    }
    return direct_to_template(request, 'meps/mep.html', context)

def mep_raw(request, mep_id):
    mep_ = MEP.view('meps/by_id', key=mep_id).first()
    jsonstr = simplejson.dumps(dict(mep_), indent=4)
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
