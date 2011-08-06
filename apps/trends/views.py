from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404

from memopol2.utils import check_dir, send_file, get_content_cache

import numpy
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot

from os.path import join

from meps.models import MEP

def trends_for_mep(request, mep_id):

    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'meps', "%s-scores.png" % mep_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    mep = get_object_or_404(MEP, id=mep_id)
    score_list = sorted(mep.score_set.all(), key=lambda k: k.proposal.date)
    scores = [s.value for s in score_list]
    of_country = [s.of_country for s in score_list]
    of_group = [s.of_group for s in score_list]
    of_ep = [s.of_ep for s in score_list]
    if not scores:
        return HttpResponseNotFound

    # blue dot
    pyplot.plot(scores, 'bo')
    a, b = numpy.polyfit(range(len(scores)), [int(x) for x in scores], 1)
    pyplot.plot([a*int(x) + b for x in range(len(scores))])
    # line
    pyplot.plot(of_country, 'y--')
    pyplot.plot(of_group, 'r--')
    pyplot.plot(of_ep, 'b--')
    pyplot.legend(('Scores', 'Median', 'Country', 'Group', 'Parliament'), 'best', shadow=True)
    pyplot.plot(scores)
    pyplot.axis([0, len(scores) - 1, 0, 102])
    pyplot.title("%s - Votes scores evolution over time" % (mep.full_name))
    pyplot.xticks(range(len(scores)), [k.proposal.short_name if k.proposal.short_name else k.proposal.date for k in score_list])
    pyplot.xlabel("Votes names or dates")
    pyplot.ylabel("Scores on votes")
    check_dir(filename)
    pyplot.savefig(filename, format="png")
    pyplot.clf()

    return send_file(request,filename, content_type="image/png")

def bar_trends_for_mep(request, mep_id):

    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'meps', "%s-bar-scores.png" % mep_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    mep = get_object_or_404(MEP, id=mep_id)
    score_list = sorted(mep.score_set.all(), key=lambda k: k.proposal.date)
    scores = [s.value for s in score_list]
    of_country = [s.of_country for s in score_list]
    of_group = [s.of_group for s in score_list]
    of_ep = [s.of_ep for s in score_list]
    if not scores:
        return HttpResponseNotFound

    #a, b = numpy.polyfit(range(len(scores)), [int(x) for x in scores], 1)
    #pyplot.plot([a*int(x) + b for x in range(len(scores))])
    # line
    pyplot.bar(map(lambda x: x+0.1, range(len(scores))), scores, width=0.2)
    pyplot.bar(map(lambda x: x+0.3, range(len(scores))), of_group, width=0.2, color="red")
    pyplot.bar(map(lambda x: x+0.5, range(len(scores))), of_ep, width=0.2, color="green")
    pyplot.bar(map(lambda x: x+0.7, range(len(scores))), of_country, width=0.2, color="yellow")
    pyplot.legend(('MEP', 'Group', 'Parliament', 'Country'), 'best', shadow=True)
    pyplot.axis([0, len(scores), 0, 102])
    pyplot.title("%s - Votes scores evolution over time" % (mep.full_name))
    pyplot.xticks(map(lambda x: x+0.5, range(len(scores))), [k.proposal.short_name if k.proposal.short_name else k.proposal.date for k in score_list])
    pyplot.xlabel("Votes names or dates")
    pyplot.ylabel("Scores on votes")
    check_dir(filename)
    pyplot.savefig(filename, format="png")
    pyplot.clf()

    return send_file(request,filename, content_type="image/png")

def comparaison_trends_for_mep(request, mep_id):

    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'meps', "%s-comparaison-scores.png" % mep_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    mep = get_object_or_404(MEP, id=mep_id)
    score_list = sorted(mep.score_set.all(), key=lambda k: k.proposal.date)
    scores = [s.value * s.proposal.ponderation for s in score_list]
    maximum = [100 * s.proposal.ponderation for s in score_list]
    #of_country = [s.of_country for s in score_list]
    of_group = [s.of_group * s.proposal.ponderation for s in score_list]
    of_ep = [s.of_ep * s.proposal.ponderation for s in score_list]
    if not scores:
        return HttpResponseNotFound

    #a, b = numpy.polyfit(range(len(scores)), [int(x) for x in scores], 1)
    #pyplot.plot([a*int(x) + b for x in range(len(scores))])
    # line
    maximum_bar = pyplot.bar(map(lambda x: x+0.3, range(len(scores))), maximum, width=0.4, color="#FFFFFF")
    for i, j in zip(map(lambda x: x+0.3, range(len(scores))), score_list):
        mep_bar = pyplot.bar(i, j.value * j.proposal.ponderation, width=0.4, color=j.color_tuple)
    #pyplot.bar(map(lambda x: x+0.3, range(len(scores))), scores, width=0.4, color=(1, 0, 0))
    group_plot, = pyplot.plot(map(lambda x: x+0.5, range(len(scores))), of_group, 'bo', markersize=10)
    ep_plot, = pyplot.plot(map(lambda x: x+0.5, range(len(scores))), of_ep, 'pg', markersize=10)
    #pyplot.text(map(lambda x: x+0.5, range(len(scores))), maximum, [s.value for s in score_list])
    for i, j, k in zip(map(lambda x: x[0]+0.28 if x[1] == 100.0 else x[0]+0.35, zip(range(len(scores)), [s.value for s in score_list])), maximum, [s.value for s in score_list]):
        pyplot.text(i - .05, j + 10, str(k) + "%")
    #pyplot.bar(map(lambda x: x+0.7, range(len(scores))), of_country, width=0.2, color="yellow")
    pyplot.legend((maximum_bar, mep_bar, ep_plot, group_plot), ('Maximum', 'MEP', 'Parliament', 'Group'), 'best', shadow=False)
    pyplot.axis([0, len(scores), 0, max(maximum) + 50])
    pyplot.title("%s - Votes scores by vote importance" % (mep.full_name))
    pyplot.yticks([])
    pyplot.xticks(map(lambda x: x+0.5, range(len(scores))), [k.proposal.short_name if k.proposal.short_name else k.proposal.date for k in score_list])
    pyplot.xlabel("Votes names or dates")
    pyplot.ylabel("Score by vote importance")
    check_dir(filename)
    pyplot.savefig(filename, format="png")
    pyplot.clf()

    return send_file(request,filename, content_type="image/png")

