from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404

from memopol2.utils import check_dir, send_file, get_content_cache

import numpy
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot

from os.path import realpath

from meps.models import MEP

def trends_for_mep(request, mep_id):

    filename = realpath(".%simg/trends/meps/%s-scores.png" % (settings.MEDIA_URL,
                                                              mep_id))
    cache = get_content_cache(request, filename)
    if cache:
        return cache

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
        check_dir(filename)
        pyplot.savefig(filename, format="png")
        pyplot.clf()
    else:
        return HttpResponseNotFound

    return send_file(request,filename, content_type="image/png")

