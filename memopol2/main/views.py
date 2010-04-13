import time
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils import simplejson

from couchdb import Server

from memopol2.main.models import Mep, Position
from memopol2 import settings

class TestFailure(Exception):
    pass



def index(request):
    couch = Server("http://localhost:5984")

    code = """
    function(d) {
        emit(null, {first: d.infos.name.first, last: d.infos.name.last});
    }
    """

    couch_meps = couch["meps"]
    meps_list = couch_meps.query(code).rows

    return render_to_response('index.html', {'meps_list': meps_list})

def mep(request, mep_id):
    mep = get_object_or_404(Mep, pk=mep_id)
    message = None
    if "pos" in request.GET:
        message = "Votre contribution a bien &eacute;t&eacute; prise en compte."

    if request.user.is_staff:
        positions = Position.objects.filter(mep=mep_id)
    else:
        positions = Position.objects.filter(mep=mep_id, visible=True)

    tdict = {'mep_id': mep_id, 'mep': mep, 'positions': positions, 'd': mep.get_couch_data(), 'message': message}

    return render_to_response('mep.html', tdict, context_instance=RequestContext(request))


def raw(request, mep_id):
    mep = get_object_or_404(Mep, pk=mep_id)
    import simplejson
    jsonstr = simplejson.dumps( mep.get_couch_data(), indent=4)
    return render_to_response('mep_raw.html', {'mep_id': mep_id, 'mep': mep, 'jsonstr': jsonstr}, context_instance=RequestContext(request))



def addposition(request, mep_id):
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
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def addposition_old(request, mep_id):
    mep = get_object_or_404(Mep, pk=mep_id)
    try:
        text = request.POST['text']
    except (KeyError):
        positions = Position.objects.filter(mep=mep_id)
        return render_to_response('mep.html', {'error_message': 'Missing POST values', 'mep_id': mep_id, 'mep': mep, 'positions': positions, 'd': mep.get_couch_data()}, context_instance=RequestContext(request))

    pos = Position(mep=mep, content=text)
    pos.submitter_username = request.user.username
    pos.submitter_ip = request.META["REMOTE_ADDR"]
    pos.submit_datetime = datetime.today()
    pos.moderated = False
    pos.visible = False
    pos.save()

    return HttpResponseRedirect(reverse('memopol2.main.views.mep', args=(mep_id,)) + "?pos")
