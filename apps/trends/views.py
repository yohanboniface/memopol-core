from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

import os

import numpy
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot

from os.path import realpath

from meps.models import MEP

def send_file(request, filename, content_type='text/plain'):
    """
    Send a file through Django.
    """
    ## Seems to no longer work with recent django
    #wrapper = FileWrapper(open(filename))
    buffer = open(filename, 'rb').read()
    response = HttpResponse(buffer, content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)
    return response

def trends_for_mep(request, mep_id):
    def save_fig(filename):
        if not os.path.exists("/".join(filename.split("/")[:-1])):
            for i in xrange(-3, 0):
                path = "/".join(filename.split("/")[:i])
                if not os.path.exists(path):
                    os.mkdir(path)
        pyplot.savefig(filename, format="png")

    filename = realpath(".%simg/trends/meps/%s-scores.png" % (settings.MEDIA_URL, mep_id))
    force = request.GET.get(u'force', '0')
    force = False if force == '0' else True

    if force or not os.path.exists(filename):
        mep = get_object_or_404(MEP, id=mep_id)
        score_list = sorted(mep.score_set.all(), key=lambda k: k.proposal.date)
        scores = [s.value for s in score_list]
        if scores:
            pyplot.plot(scores, 'bo')
            a, b = numpy.polyfit(range(len(scores)), [int(x) for x in scores], 1)
            pyplot.plot([a*int(x) + b for x in range(len(scores))])
            pyplot.legend(('Scores', 'Mediane'), 'best', shadow=True)
            pyplot.plot(scores)
            pyplot.axis([0, len(scores) - 1, 0, 102])
            pyplot.title("%s - Votes notes evolution over time" % (mep.full_name))
            pyplot.xticks(range(len(scores)), [k.proposal.date for k in score_list])
            pyplot.xlabel("Votes dates")
            pyplot.ylabel("Scores on votes")
            save_fig(filename)
            pyplot.clf()
        else:
            return HttpResponseNotFound

    print "send file"
    return send_file(request,filename, content_type="image/png")

