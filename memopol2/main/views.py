import time
from datetime import datetime

from django.http import HttpResponse, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.core import serializers

from django.contrib.admin.views.decorators import staff_member_required

from couchdbkit import Server

from memopol2.main.models import Mep, Position
from memopol2 import settings
from memopol2.util import get_couch_doc_or_404

def index_names(request):
    couch = Server(settings.COUCHDB)

    map_fun = """
    function(d) {
        emit(null, {first: d.infos.name.first, last: d.infos.name.last, group: d.infos.group.abbreviation});
    }
    """

    couch_meps = couch["meps"]
    meps_list = couch_meps.temp_view({"map": map_fun})
    meps_list.fetch()
    meps_list = meps_list.all()

    return render_to_response('index.html', {'meps_list': meps_list}, context_instance=RequestContext(request))

def index_groups(request):
    couch = Server(settings.COUCHDB)

    map_fun = """
    function(d) {
        emit(d.infos.group.abbreviation, { name: d.infos.group.name,  count: 1 });
    }
    """

    reduce_fun = """function(keys, values) {
        var sum = 0;
        for (var idx in values)
        {
            sum += values[idx].count;
        }
        return {name: values[0].name , count: sum};
    }"""

    couch_meps = couch["meps"]
    groups = couch_meps.temp_view({"map": map_fun, "reduce": reduce_fun}, group="true")
    groups.fetch()
    groups = groups.all()

    return render_to_response('index.html', {'groups': groups}, context_instance=RequestContext(request))

def index_countries(request):
    couch = Server(settings.COUCHDB)

    map_fun = """
    function(d) {
        emit(d.infos.constituency.country.name, { code: d.infos.constituency.country.code, count: 1 });
    }
    """

    reduce_fun = """function(keys, values) {
        var sum = 0;
        for (var idx in values)
        {
            sum += values[idx].count;
        }
        return {code: values[0].code, count: sum};
    }"""

    couch_meps = couch["meps"]
    
    req = couch_meps.temp_view({"map": map_fun, "reduce": reduce_fun }, group=True)
    req.fetch()
    countries = req.all()

    return render_to_response('index.html', {'countries': countries}, context_instance=RequestContext(request))

def index_by_country(request, country_code):
    country_code = country_code.upper()
    couch = Server(settings.COUCHDB)

    map_fun = """
    function(d) {
        if (d.infos.constituency.country.code)
        {
            emit(d.infos.constituency.country.code, {first: d.infos.name.first, last: d.infos.name.last, group: d.infos.group.abbreviation});
        }
    }
    """

    couch_meps = couch["meps"]
    req = couch_meps.temp_view({"map": map_fun}, key=country_code)
    req.fetch()
    meps_list = req.all()

    return render_to_response('index.html', {'meps_list': meps_list}, context_instance=RequestContext(request))

def index_by_group(request, group):
    couch = Server(settings.COUCHDB)

    map_fun = """
    function(d) {
        if (d.infos.group.abbreviation)
        {
            emit(d.infos.group.abbreviation, {first: d.infos.name.first, last: d.infos.name.last, group: d.infos.group.abbreviation});
        }
    }
    """

    couch_meps = couch["meps"]
    meps_list = couch_meps.temp_view({"map": map_fun}, key=group)
    meps_list.fetch()
    meps_list = meps_list.all()

    return render_to_response('index.html', {'meps_list': meps_list}, context_instance=RequestContext(request))


def mep(request, mep_id):
    data = get_couch_doc_or_404(Mep, mep_id)
    ctx = {'mep_id': mep_id, 'mep': mep, 'd': data }
    ctx['positions'] = Position.objects.filter(mep_id=mep_id)
    ctx['visible_count'] = len([ x for x in ctx['positions'] if x.visible ])
    return render_to_response('mep.html', ctx, context_instance=RequestContext(request))

def mep_raw(request, mep_id):
    mep_ = get_couch_doc_or_404(Mep, mep_id)
    jsonstr = simplejson.dumps(mep_, indent=4)
    ctx = {'mep_id': mep_id, 'mep': mep_, 'jsonstr': jsonstr}
    return render_to_response('mep_raw.html', ctx, context_instance=RequestContext(request))

def mep_addposition(request, mep_id):
    if not request.is_ajax():
        return HttpResponseServerError()
    results = {'success':False}
    # make sure the mep exists
    mep_ = get_couch_doc_or_404(Mep, mep_id)
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
    ctx = {}
    ctx['positions'] = Position.objects.filter(moderated=False)
    return render_to_response('moderation.html', ctx, context_instance=RequestContext(request))

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

