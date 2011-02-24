import time
from datetime import datetime

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.core import serializers
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib.admin.views.decorators import staff_member_required

from memopol2.main.models import Position, Database, Vote

def index_names(request):
    meps_by_name = Database().get_meps_by_names()
    context = {
        'meps': meps_by_name,
    }
    return direct_to_template(request, 'index.html', context)

def index_groups(request):
    groups = Database().get_groups()
    context = {
        'groups': groups,
    }
    return direct_to_template(request, 'index.html', context)

def index_countries(request):
    countries = Database().get_countries()
    context = {
        'countries': countries,
    }
    return direct_to_template(request, 'index.html', context)

def index_by_country(request, country_code):
    meps_by_country = Database().get_meps_by_country(country_code)
    context = {
        'meps': meps_by_country,
    }
    return direct_to_template(request, 'index.html', context)

def index_by_group(request, group):
    meps_by_group = Database().get_meps_by_group(group)
    context = {
        'meps': meps_by_group,
    }
    return direct_to_template(request, 'index.html', context)

def mep(request, mep_id):
    data = Database().get_mep(mep_id)
    positions = Position.objects.filter(mep_id=mep_id)
    context = {
        'mep_id': mep_id,
        'data': data,
        'positions': positions,
        'visible_count': len([x for x in positions if x.visible]),
    }
    return direct_to_template(request, 'mep.html', context)

def mep_raw(request, mep_id):
    mep_ = Database().get_mep(mep_id)
    jsonstr = simplejson.dumps(mep_, indent=4)
    context = {
        'mep_id': mep_id, 
        'mep': mep_, 
        'jsonstr': jsonstr,
    }
    return direct_to_template(request, 'mep_raw.html', context)

def mep_addposition(request, mep_id):
    if not request.is_ajax():
        return HttpResponseServerError()
    results = {'success':False}
    # make sure the mep exists
    mep_ = Database().get_mep(mep_id)
    try:
        text = request.GET[u'text']
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
    return direct_to_template(request, 'moderation.html', context)

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

def index_votes(request):
    votes = Vote.view('main/all')
    context = {
        'votes': votes,
    }
    return direct_to_template(request, 'votes.html', context)

def vote(request, vote_name):
    votes = Vote.view('main/all')
    context = {
        'vote': [vote for vote in votes.all() if vote.wiki==vote_name][0],
    }
    return direct_to_template(request, 'vote.html', context)

