import time
from datetime import datetime
import simplejson

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.core import serializers

from django.contrib.admin.views.decorators import staff_member_required

from couchdb import Server

from memopol2.main.models import Mep, Position
from memopol2 import settings
from memopol2.util import *

def index(request):
    couch = Server("http://localhost:5984")

    code = """
    function(d) {
        emit(null, {first: d.infos.name.first, last: d.infos.name.last});
    }
    """

    couch_meps = couch["meps"]
    meps_list = couch_meps.query(code).rows

    return render_to_response('index.html', {'meps_list': meps_list}, context_instance=RequestContext(request))

def mep(request, mep_id):
    mep = get_object_or_404(Mep, pk=mep_id)
    ctx = {'mep_id': mep_id, 'mep': mep, 'd': mep.get_couch_data() }
    ctx['positions'] = Position.objects.filter(mep=mep_id)
    ctx['visible_count'] = len([ x for x in ctx['positions'] if x.visible ])
    return render_to_response('mep.html', ctx, context_instance=RequestContext(request))

def mep_raw(request, mep_id):
    mep = get_object_or_404(Mep, pk=mep_id)
    jsonstr = simplejson.dumps( mep.get_couch_data(), indent=4)
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

