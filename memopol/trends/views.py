import re
import os

from django.conf import settings
from django.db.models import Avg
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext, get_language

from memopol.base.utils import check_dir, send_file, get_content_cache, color

import numpy
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot

from os.path import join

from memopol.meps.models import MEP, Group, Country
from memopol.votes.models import Recommendation, Vote, Score, Proposal

def trends_for_mep(request, mep_id):

    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'meps', get_language() + "-%s-scores.png" % mep_id)
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
    pyplot.legend((ugettext('Scores'), ugettext('Median'), ugettext('Country'), ugettext('Group'), ugettext('Parliament')), 'best', shadow=True)
    pyplot.plot(scores)
    pyplot.axis([0, len(scores) - 1, 0, 102])
    pyplot.title(ugettext("%(mep_name)s - Votes scores evolution over time") % {"mep_name": mep.full_name})
    pyplot.xticks(range(len(scores)), [k.proposal.short_name if k.proposal.short_name else k.proposal.date for k in score_list], rotation=-17)
    pyplot.xlabel(ugettext("Votes names or dates"))
    pyplot.ylabel(ugettext("Scores on votes"))
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.clf()

    return send_file(request,filename, content_type="image/png")

def bar_trends_for_mep(request, mep_id):

    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'meps', get_language() + "-%s-bar-scores.png" % mep_id)
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
    pyplot.legend((ugettext('MEP'), ugettext('Group'), ugettext('Parliament'), ugettext('Country')), 'best', shadow=True)
    pyplot.axis([0, len(scores), 0, 102])
    pyplot.title(ugettext("%(mep_name)s - Votes scores evolution over time") % {"mep_name": mep.full_name})
    pyplot.xticks(map(lambda x: x+0.5, range(len(scores))), [k.proposal.short_name if k.proposal.short_name else k.proposal.date for k in score_list], rotation=-17)
    pyplot.xlabel(ugettext("Votes names or dates"))
    pyplot.ylabel(ugettext("Scores on votes"))
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.clf()

    return send_file(request,filename, content_type="image/png")

def comparaison_trends_for_mep(request, mep_id):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'meps', get_language() + "-%s-comparaison-scores.png" % mep_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    mep = get_object_or_404(MEP, id=mep_id)
    score_list = sorted(mep.score_set.all(), key=lambda k: k.proposal.date)
    scores = [s.value * s.proposal.ponderation for s in score_list]
    if not scores:
        return HttpResponseNotFound
    maximum = [100 * s.proposal.ponderation for s in score_list]
    center = [x+0.5 for x in range(len(scores))]
    of_group = [s.of_group * s.proposal.ponderation for s in score_list]
    of_ep = [s.of_ep * s.proposal.ponderation for s in score_list]


    maximum_bar = pyplot.bar(center, maximum, width=0.4, color="#FFFFFF", align='center')
    mep_bar = pyplot.bar(center, scores, width=0.4, color=map(lambda z: map(lambda y: y/255., z.color_tuple), score_list), align='center')
    group_plot, = pyplot.plot(center, of_group, 'bo', markersize=10)
    ep_plot, = pyplot.plot(center, of_ep, 'pg', markersize=10)
    for i, j, k in zip(center, maximum, [s.value for s in score_list]):
        pyplot.text(i+0.02, j+18, str(k) + "%", horizontalalignment='center', verticalalignment='center')

    pyplot.legend((maximum_bar, mep_bar, ep_plot, group_plot), (ugettext('Maximum'), ugettext('MEP'), ugettext('Parliament'), ugettext('Group')), 'best', shadow=False)
    pyplot.axis([0, len(scores), 0, max(maximum) + 50])
    pyplot.title(ugettext("%(mep_name)s - Votes scores by vote importance") % {"mep_name": mep.full_name})
    pyplot.yticks([])
    pyplot.xticks(map(lambda x: x+0.5, range(len(scores))), [k.proposal.short_name if k.proposal.short_name else k.proposal.date for k in score_list], rotation=-17)
    pyplot.xlabel(ugettext("Votes names or dates"))
    pyplot.ylabel(ugettext("Score by vote importance"))
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.clf()

    return send_file(request, filename, content_type="image/png")

def recommendation_group(request, recommendation_id):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'recommendations', get_language() + "-%s-group.png" % recommendation_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    recommendation = get_object_or_404(Recommendation, id=recommendation_id)

    if recommendation.recommendation == "for":
        for_color = "#00FF00"
        against_color = "#FF0000"
    else:
        against_color = "#00FF00"
        for_color = "#FF0000"

    groups = []
    a = 0
    for group in Group.objects.order_by('abbreviation'):
        votes = Vote.objects.filter(recommendation=recommendation, representative__mep__groupmep__group=group, representative__mep__groupmep__begin__lte=recommendation.proposal.date, representative__mep__groupmep__end__gte=recommendation.proposal.date)
        if not votes:
            votes = Vote.objects.filter(recommendation=recommendation, representative__mep__groupmep__group=group)
        if votes.count():
            _for = votes.filter(choice="for").count()
            abstention = votes.filter(choice="abstention").count()
            against = votes.filter(choice="against").count()
            # not present
            pyplot.bar(a + 0.1, group.meps_on_date(recommendation.proposal.date).count() - against - _for - abstention, width=0.8, bottom=against + abstention + _for, color="#AAAAAA")
            # against
            pyplot.bar(a + 0.1, against, width=0.8, bottom=abstention + _for, color=against_color)
            # abstention
            pyplot.bar(a + 0.1, abstention, width=0.8, bottom=_for, color="#FF8800")
            # for
            pyplot.bar(a + 0.1, _for, width=0.8, color=for_color)
            groups.append(group.abbreviation)
            a += 1

    pyplot.legend((ugettext('Not present'),ugettext('against'), ugettext('abstention'), ugettext('for')), 'best', shadow=False)
    pyplot.title(ugettext("Group vote repartition"))
    pyplot.xticks(map(lambda x: x+0.5, range(len(groups))), groups, rotation=-17)
    pyplot.xlabel(ugettext("Groups"))
    pyplot.ylabel(ugettext("Number of meps"))
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.clf()

    return send_file(request, filename, content_type="image/png")

def proposal_countries_map(request, proposal_id, extension):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'proposal', "%s-countries-map.%s" % (proposal_id, extension))
    cache = get_content_cache(request, filename)
    if cache:
        if extension == "png":
            return HttpResponse(cache, mimetype="image/png")
        return HttpResponse(cache, mimetype="image/svg+xml")

    proposal = get_object_or_404(Proposal, id=proposal_id)

    countries = {}

    for country in Country.objects.order_by('code'):
        countries[country.code] = Score.objects.filter(proposal=proposal, representative__mep__countrymep__country=country).aggregate(average_score=Avg('value'))['average_score']

    current_country = None
    out = ""
    for line in open(join(settings.STATIC_ROOT, "svg", "grey_europe_map.svg"), "r").readlines():

        if '         {}' in line:
            get = re.match('.*([a-z][a-z]).*', line)

            if get and get.group(1).upper() in countries.keys():
                current_country = get.group(1).upper()

        # HAHAHAHA blam those who can't write a human uzable xml lib for python
        if current_country:
            if countries[current_country]:
                line = re.sub("{}", "{fill:rgb(%s, %s, %s);}" % color(countries[current_country]), line)
            current_country = None

        out += line

    check_dir(filename)
    open(filename, "w").write(out)

    if extension == "png":
        png_filename = ".".join(filename.split(".")[:-1]) + ".png"
        os.system("convert %s %s" % (filename, png_filename))
        return HttpResponse(open(png_filename).read(), mimetype="image/png")

    return HttpResponse(out, mimetype="image/svg+xml")

def recommendation_countries(request, recommendation_id):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'recommendations', get_language() + "-%s-countries.png" % recommendation_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    recommendation = get_object_or_404(Recommendation, id=recommendation_id)

    if recommendation.recommendation == "for":
        for_color = "#00FF00"
        against_color = "#FF0000"
    else:
        against_color = "#00FF00"
        for_color = "#FF0000"

    max_total = 0
    countries = []
    a = 0
    no_date = False
    for country in Country.objects.order_by('code'):
        votes = Vote.objects.filter(recommendation=recommendation, representative__mep__countrymep__country=country, representative__mep__countrymep__begin__lte=recommendation.proposal.date, representative__mep__countrymep__end__gte=recommendation.proposal.date).distinct()
        if not votes:
            votes = Vote.objects.filter(recommendation=recommendation, representative__mep__countrymep__country=country).distinct()
            no_date = True
        if votes.count():
            if not no_date:
                all_meps = country.meps_on_date(recommendation.proposal.date).distinct().count()
            else:
                all_meps = country.meps.distinct().count()
            if all_meps > max_total:
                max_total = all_meps
            _for = votes.filter(choice="for").distinct().count()
            abstention = votes.filter(choice="abstention").distinct().count()
            against = votes.filter(choice="against").distinct().count()
            ## not present
            pyplot.bar(a + 0.1, all_meps - _for - abstention - against, width=0.8, bottom=_for + abstention + against , color="#AAAAAA")
            ## against
            pyplot.bar(a + 0.1, against, width=0.8, bottom=_for + abstention, color=against_color)
            ## abstention
            pyplot.bar(a + 0.1, abstention, width=0.8, bottom=_for, color="#FF8800")
            ## for
            pyplot.bar(a + 0.1, _for, width=0.8, color=for_color)
            countries.append(country.code)
            a += 1

    pyplot.legend((ugettext('Not present'), ugettext('against'), ugettext('abstention'), ugettext('for')), 'best', shadow=False)
    pyplot.title(ugettext("Countries vote repartition on %(recommendation_part)s for %(recommandation_proposal)s") % {"recommendation_part": recommendation.part, "recommandation_proposal": recommendation.proposal.short_name if recommendation.proposal.short_name else recommendation.proposal.title})
    pyplot.xticks(map(lambda x: x+0.5, range(len(countries))), countries)
    pyplot.xlabel(ugettext("Countries"))
    pyplot.ylabel(ugettext("Number of meps"))
    pyplot.axis([0, len(countries), 0, max_total + 2])
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.clf()

    return send_file(request, filename, content_type="image/png")

def recommendation_countries_absolute(request, recommendation_id):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'recommendations', get_language() + "-%s-countries-absolute.png" % recommendation_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    recommendation = get_object_or_404(Recommendation, id=recommendation_id)

    if recommendation.recommendation == "for":
        for_color = "#00FF00"
        against_color = "#FF0000"
    else:
        against_color = "#00FF00"
        for_color = "#FF0000"

    countries = []
    a = 0
    no_date = False
    for country in Country.objects.order_by('code'):
        votes = Vote.objects.filter(recommendation=recommendation, representative__mep__countrymep__country=country, representative__mep__countrymep__begin__lte=recommendation.proposal.date, representative__mep__countrymep__end__gte=recommendation.proposal.date).distinct()
        if not votes:
            no_date = True
            votes = Vote.objects.filter(recommendation=recommendation, representative__mep__countrymep__country=country).distinct()

        if votes.count():
            if not no_date:
                all_meps = country.meps_on_date(recommendation.proposal.date).distinct().count()
            else:
                all_meps = country.meps.distinct().count()
            _for = votes.filter(choice="for").distinct().count()
            against = votes.filter(choice="against").distinct().count()
            abstention = votes.filter(choice="abstention").distinct().count()
            pyplot.bar(a + 0.1, 100, width=0.8, bottom= (against + abstention + _for) * 100. / all_meps, color="#AAAAAA")
            ## against
            pyplot.bar(a + 0.1, against * 100. / all_meps, width=0.8, bottom= (abstention + _for) * 100. / all_meps, color=against_color)
            ## abstention
            pyplot.bar(a + 0.1, abstention * 100. / all_meps, width=0.8, bottom= _for * 100. / all_meps, color="#FF8800")
            ## for
            pyplot.bar(a + 0.1, _for * 100. / all_meps, width=0.8, color=for_color)
            countries.append(country.code)
            a += 1

    #pyplot.legend((ugettext('Not present'), ugettext('against'), ugettext('abstention'), ugettext('for')), 'best', shadow=False)
    pyplot.title(ugettext("Normalized countries vote repartition on %(recommendation_part)s for %(recommendation_proposal)s") % {"recommendation_part": recommendation.part, "recommendation_proposal": recommendation.proposal.short_name if recommendation.proposal.short_name else recommendation.proposal.title})
    pyplot.xticks(map(lambda x: x+0.5, range(len(countries))), countries)
    pyplot.xlabel(ugettext("Countries"))
    pyplot.ylabel(ugettext("% of choices"))
    pyplot.axis([0, len(countries), 0, 100])
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.clf()

    return send_file(request, filename, content_type="image/png")

def group_proposal_score_repartition(request, group_abbreviation, proposal_id):
    group_id = group_abbreviation
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'group', get_language() + "-%s-%s-repartition.png" % (group_id, proposal_id))
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    group = get_object_or_404(Group, abbreviation=group_id)
    proposal = get_object_or_404(Proposal, id=proposal_id)

    maxeu = 0
    #for mep in MEP.objects.filter(score__proposal=proposal, groupmep__group=group):
    scores = []
    for score_range in range(0, 100, 5):
        meps = group.mep_set.filter(groupmep__end__gte=proposal.date, groupmep__begin__lte=proposal.date, score__proposal=proposal, score__value__lt=score_range + 5, score__value__gte=score_range).distinct().count()
        if meps > maxeu:
            maxeu = meps
        #pyplot.bar(score_range/10 + 0.1, meps, color=map(lambda x: x/255., color(score_range + 5)))
        scores.append((score_range, meps))

    scores.append((100, group.mep_set.filter(groupmep__end__gte=proposal.date, groupmep__begin__lte=proposal.date, score__proposal=proposal, score__value=100).distinct().count()))
    pyplot.plot(*zip(*scores))

    #pyplot.legend(('MEPs',), 'best', shadow=False)
    pyplot.title(ugettext("Score repartition for %(abbr)s on %(proposal)s") % {"abbr": group.abbreviation, "proposal": proposal.short_name if proposal.short_name else proposal.title})
    pyplot.xticks(range(0, 105, 5), range(0, 105, 5))
    pyplot.xlabel(ugettext("Score range 5 by 5"))
    pyplot.ylabel(ugettext("MEPs"))
    #pyplot.axis([0, 20.1, 0, maxeu + 3])
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.clf()

    return send_file(request, filename, content_type="image/png")

def proposal_score_repartition(request, proposal_id):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'group', get_language() + "-%s-repartition.png" % proposal_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    proposal = get_object_or_404(Proposal, id=proposal_id)

    maxeu = 0
    #scores = [(0, MEP.objects.filter(groupmep__end__gte=proposal.date, groupmep__begin__lte=proposal.date, score__proposal=proposal, score__value=0).distinct().count())]
    scores = []
    #for mep in MEP.objects.filter(score__proposal=proposal, groupmep__group=group):
    for score_range in range(0, 100, 5):
        meps = MEP.objects.filter(groupmep__end__gte=proposal.date, groupmep__begin__lte=proposal.date, score__proposal=proposal, score__value__lt=score_range + 5, score__value__gte=score_range).distinct().count()
        if meps > maxeu:
            maxeu = meps
        scores.append((score_range, meps))
        #pyplot.bar(score_range/10 + 0.1, meps, color=map(lambda x: x/255., color(score_range + 5)))

    scores.append((100, MEP.objects.filter(groupmep__end__gte=proposal.date, groupmep__begin__lte=proposal.date, score__proposal=proposal, score__value=100).distinct().count()))
    pyplot.plot(*zip(*scores))

    #pyplot.legend((ugettext('MEPs'),), 'best', shadow=False)
    pyplot.title(ugettext("Score repartition on %(proposal)s") % {"proposal": proposal.short_name if proposal.short_name else proposal.title})
    pyplot.xticks(range(0, 105, 5), range(0, 105, 5))
    pyplot.xlabel(ugettext("Score range 5 by 5"))
    pyplot.ylabel(ugettext("MEPs"))
    #pyplot.axis([0, 10.1, 0, maxeu + 3])
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.clf()

    return send_file(request, filename, content_type="image/png")

def group_proposal_score(request, proposal_id):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'group', get_language() + "-groups-%s-repartition.png" % proposal_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    proposal = get_object_or_404(Proposal, id=proposal_id)

    group_color = {'ALDE': '#FFFF00',
                   'ELDR': '#FFFF00',
                   'ECR': '#000084',
                   'EFD': '#48D1CC',
                   'GUE/NGL': '#9C0000',
                   'IND/DEM': '#FF9900',
                   'EDD': '#FF9900',
                   'NI': '#848284',
                   'EPP': '#319AFF',
                   'PPE-DE': '#319AFF',
                   'SD': '#FF0000',
                   'PSE': '#FF0000',
                   'Greens/EFA': '#009A00',
                   'ITS': '#000000',
                   'UEN': '#05FBEE'}

    group_bar = {}

    maxeu = 0
    #for mep in MEP.objects.filter(score__proposal=proposal, groupmep__group=group):
    a = 0.1
    for group in proposal.groups:
        for score_range in range(0, 100, 10):
            meps = group.mep_set.filter(groupmep__end__gte=proposal.date, groupmep__begin__lte=proposal.date, score__proposal=proposal, score__value__lt=score_range + 10 if score_range != 90 else 101, score__value__gte=score_range).distinct().count()
            if meps > maxeu:
                maxeu = meps
            group_bar[group.abbreviation] = pyplot.bar(score_range/10 + a, meps, width=0.1, color=group_color.get(group.abbreviation, '#FFFFFF'))
        a += .1

    a, b = zip(*group_bar.items())
    pyplot.legend(list(b), list(a), 'best', shadow=False)
    pyplot.title(ugettext("Score repartition for groups on %(proposal)s") % {"proposal": proposal.short_name if proposal.short_name else proposal.title})
    pyplot.xticks(range(11), range(0, 110, 10))
    pyplot.xlabel(ugettext("Score range 10 by 10"))
    pyplot.ylabel(ugettext("MEPs per group"))
    pyplot.axis([0, 10.1, 0, maxeu + 3])
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.clf()

    return send_file(request, filename, content_type="image/png")

def group_proposal_score_stacked(request, proposal_id):
    filename = join(settings.MEDIA_DIRECTORY, 'img', 'trends', 'group', get_language() + "-groups-%s-repartition-stacked.png" % proposal_id)
    pyplot.figure(figsize=(8, 8))
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    proposal = get_object_or_404(Proposal, id=proposal_id)

    if proposal.institution != "EU":
        return HttpResponse("")

    group_color = {'ALDE': '#FFFF00',
                   'ELDR': '#FFFF00',
                   'ECR': '#000084',
                   'EFD': '#48D1CC',
                   'GUE/NGL': '#9C0000',
                   'IND/DEM': '#FF9900',
                   'EDD': '#FF9900',
                   'NI': '#848284',
                   'EPP': '#319AFF',
                   'PPE-DE': '#319AFF',
                   'SD': '#FF0000',
                   'PSE': '#FF0000',
                   'Greens/EFA': '#009A00',
                   'ITS': '#000000',
                   'UEN': '#05FBEE'}

    group_bar = {}

    maxeu = 0

    #for mep in MEP.objects.filter(score__proposal=proposal, groupmep__group=group):
    for score_range in range(0, 100, 10):
        limit=0
        for group in proposal.groups:
            meps = group.mep_set.filter(groupmep__end__gte=proposal.date, groupmep__begin__lte=proposal.date, score__proposal=proposal, score__value__lt=score_range + 10 if score_range != 90 else 101, score__value__gte=score_range).distinct().count()
            if not meps:
                meps = group.mep_set.filter(score__proposal=proposal, score__value__lt=score_range + 10 if score_range != 90 else 101, score__value__gte=score_range).distinct().count()
            group_bar[group.abbreviation] = pyplot.bar(score_range/10 + 0.1, meps, width=0.8, bottom=limit, color=group_color.get(group.abbreviation, '#FFFFFF'))
            limit+=meps

    a, b = zip(*group_bar.items())
    pyplot.legend(list(b), list(a), 'best', shadow=False)
    pyplot.title(ugettext("Score repartition for groups on %(proposal)s") % {"proposal": proposal.short_name if proposal.short_name else proposal.title})
    pyplot.xticks(range(11), range(0, 110, 10))
    pyplot.xlabel(ugettext("Score on vote (range 10 by 10)"))
    pyplot.ylabel(ugettext("Number of MEPs (by political group) with X points (for this vote)"))
    #pyplot.axis([0, 10.1, 0, maxeu + 3])
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.figure(figsize=(8, 6))
    pyplot.clf()

    return send_file(request, filename, content_type="image/png")

def group_proposal_score_heatmap(request, proposal_id):
    filename = join(settings.STATIC_ROOT, 'img', 'trends', 'group', get_language() + "-groups-%s-repartition-heatmap.png" % proposal_id)
    cache = get_content_cache(request, filename)
    if cache:
        return cache

    proposal = get_object_or_404(Proposal, id=proposal_id)
    countries= proposal.countries
    groups = proposal.groups

    if proposal.institution != "EU":
        return HttpResponse("")

    fig = pyplot.figure(figsize=(len(countries) / 2.8, len(groups) / 2.8))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, len(proposal.countries))
    ax.set_ylim(0, len(groups))

    biggest_group_of_a_country = 0
    for country in countries:
        for group in groups:
            meps = MEP.objects.filter(score__proposal=proposal,
                                      groupmep__end__gte=proposal.date,
                                      groupmep__begin__lte=proposal.date,
                                      countrymep__begin__lte=proposal.date,
                                      countrymep__end__gte=proposal.date,
                                      countrymep__country=country,
                                      groupmep__group=group).distinct().count()

            if not meps:
                meps = MEP.objects.filter(score__proposal=proposal,
                                          countrymep__country=country,
                                          groupmep__group=group).distinct().count()

            if meps > biggest_group_of_a_country:
                biggest_group_of_a_country = meps

    biggest_group_of_a_country = float(biggest_group_of_a_country)

    a = 0.5
    for country in countries:
        b = 0.5
        for group in groups:
            meps = MEP.objects.filter(score__proposal=proposal,
                                      groupmep__end__gte=proposal.date,
                                      groupmep__begin__lte=proposal.date,
                                      countrymep__begin__lte=proposal.date,
                                      countrymep__end__gte=proposal.date,
                                      countrymep__country=country,
                                      groupmep__group=group).distinct().count()

            if not meps:
                meps = MEP.objects.filter(score__proposal=proposal,
                                          countrymep__country=country,
                                          groupmep__group=group).distinct().count()

            score = Score.objects.filter(proposal=proposal,
                                         representative__mep__groupmep__group=group,
                                         representative__mep__groupmep__begin__lte=proposal.date,
                                         representative__mep__groupmep__end__gte=proposal.date,
                                         representative__mep__countrymep__country=country,
                                         representative__mep__countrymep__begin__lte=proposal.date,
                                         representative__mep__countrymep__end__gte=proposal.date).aggregate(Avg('value'))['value__avg']

            if not score:
                score = Score.objects.filter(proposal=proposal,
                                             representative__mep__groupmep__group=group,
                                             representative__mep__countrymep__country=country).aggregate(Avg('value'))['value__avg']

            if score:
                ax.scatter(a, b, s=280*(meps/biggest_group_of_a_country),
                             c=map(lambda x: x/255., color(score)),
                             alpha=0.6)

            b += 1
        a += 1

    pyplot.title(ugettext("Heatmap of group/country on %(proposal)s") % {"proposal": proposal.short_name if proposal.short_name else proposal.title})

    pyplot.xticks(map(lambda x: x + 0.5, range(len(countries))), map(lambda x: x.code, countries))
    pyplot.yticks(map(lambda x: x + 0.5, range(len(groups))), map(lambda x: x.abbreviation, groups))
    check_dir(filename)
    pyplot.savefig(filename, format="png", bbox_inches='tight')
    pyplot.figure(figsize=(8, 6))
    pyplot.clf()

    return send_file(request, filename, content_type="image/png")
