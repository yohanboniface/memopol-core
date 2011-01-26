import time
from datetime import datetime

from django.http import HttpResponse, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.core import serializers

from django.contrib.admin.views.decorators import staff_member_required

from couchdb import Server

from memopol2.main.models import Mep, Position
from memopol2 import settings
from memopol2.util import *

def index_names(request):
    couch = Server(settings.COUCHDB)

    code = """
    function(d) {
        emit(null, {first: d.infos.name.first, last: d.infos.name.last});
    }
    """

    couch_meps = couch["meps"]
    meps_list = couch_meps.query(code).rows

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
    groups = couch_meps.query(map_fun, reduce_fun, "javascript", group="true").rows

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
    countries = couch_meps.query(map_fun, reduce_fun, "javascript", group="true").rows

    return render_to_response('index.html', {'countries': countries}, context_instance=RequestContext(request))

def index_by_country(request, country_code):
    country_code = country_code.upper()
    couch = Server(settings.COUCHDB)

    code = """
    function(d) {
        if (d.infos.constituency.country.code)
        {
            emit(d.infos.constituency.country.code, {first: d.infos.name.first, last: d.infos.name.last, group: d.infos.group.abbreviation});
        }
    }
    """

    couch_meps = couch["meps"]
    meps_list = couch_meps.query(code, key=country_code).rows

    return render_to_response('index.html', {'meps_list': meps_list}, context_instance=RequestContext(request))

def index_by_group(request, group):
    couch = Server(settings.COUCHDB)

    code = """
    function(d) {
        if (d.infos.group.abbreviation)
        {
            emit(d.infos.group.abbreviation, {first: d.infos.name.first, last: d.infos.name.last});
        }
    }
    """

    couch_meps = couch["meps"]
    meps_list = couch_meps.query(code, key=group).rows

    return render_to_response('index.html', {'meps_list': meps_list}, context_instance=RequestContext(request))

def fixup_mep(mepdata):
    # fixup email.addr.text
    try:
        node = mepdata["contact"]["email"]
        if not(type(node) is dict and node.has_key("text")):
            mepdata["contact"]["email"] = { "text": node }
    except Exception:
        raise
    return mepdata

def mep(request, mep_id):
    mep = get_object_or_404(Mep, pk=mep_id)
    data = fixup_mep(mep.get_couch_data())
    ctx = {'mep_id': mep_id, 'mep': mep, 'd': data }
    ctx['positions'] = Position.objects.filter(mep=mep_id)
    ctx['visible_count'] = len([ x for x in ctx['positions'] if x.visible ])
    return render_to_response('mep.html', ctx, context_instance=RequestContext(request))

def mep_raw(request, mep_id):
    mep = get_object_or_404(Mep, pk=mep_id)
    data = fixup_mep(mep.get_couch_data())
    jsonstr = simplejson.dumps( data, indent=4)
    return render_to_response('mep_raw.html', {'mep_id': mep_id, 'mep': mep, 'jsonstr': jsonstr}, context_instance=RequestContext(request))

def mep_addposition(request, mep_id):
    if not request.is_ajax():
        return HttpResponseServerError()
    results = {'success':False}
    mep = get_object_or_404(Mep, pk=mep_id)
    try:
        text = request.GET[u'text']
        if settings.DEBUG:
            if 'slow' in text:
                time.sleep(10)
            if 'fail' in text:
                raise TestFailure()
        pos = Position(mep=mep, content=text)
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
    try:
        position = get_object_or_404(Position, pk=int(request.GET[u'pos_id']))
        position.moderated = True
        position.visible = (request.GET[u'decision'] == "1")
        position.save()
        results = {'success':True}
    except:
        pass
    return HttpResponse(simplejson.dumps(results), mimetype='application/json')

