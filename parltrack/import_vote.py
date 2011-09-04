#!/usr/bin/python
# -*- coding:Utf-8 -*-

import re
import sys
import json

from urllib import urlopen
from datetime import datetime, time

from django.conf import settings

from meps.utils import update_total_score_of_all_meps
from meps.models import MEP
from votes.utils import clean_all_trends
from votes.models import RecommendationData, Proposal, Recommendation, Vote, Score

from check_vote import check_recommendationdata

def get_proposal(proposal_name):
    proposal = Proposal.objects.filter(title=proposal_name)
    if proposal:
        proposal = proposal[0]
    else:
        _id = raw_input("Chose a proposal id (only letter and _) for '%s'\n>>> " % proposal_name)
        while not re.match("^[0-9A-Za-z_]+$", _id):
            _id = raw_input("Bad input, chose a proposal id (only letter and _) for '%s'\n>>> ")
        proposal = Proposal.objects.filter(id=_id)
        if proposal:
            print "Get proposal that already exist with this id"
            proposal = proposal[0]
        else:
            print "Create new proposal"
            proposal = Proposal.objects.create(title=proposal_name, id=_id, institution="EU")
    return proposal

def create_recommendation(recommendationdata_id, choice, weight):
    rd = RecommendationData.objects.get(id=recommendationdata_id)
    data = json.loads(rd.data)
    Recommendation.objects.filter(datetime=datetime.combine(rd.date, time()),
                                  subject="".join(rd.title.split("-")[:-1]),
                                  part=data["issue_type"],
                                  weight=int(weight),
                                  recommendation=choice).delete()
    proposal = get_proposal(rd.proposal_name)
    print "Creating recommendation"
    r = Recommendation.objects.create(datetime=datetime.combine(rd.date, time()),
                                  subject="".join(rd.title.split("-")[:-1]),
                                  part=data["issue_type"],
                                  weight=int(weight),
                                  proposal=proposal,
                                  recommendation=choice)

    choices = (('Against', 'against'), ('For', 'for'), ('Abstain', 'abstention'))
    # clean old votes
    a = 0
    Vote.objects.filter(recommendation=r).delete()
    for key, choice in choices:
        for group in data[key]["groups"]:
            for mep in group["votes"]:
                mep = mep["orig"]
                mep = mep.replace(u"ß", "SS")
                print settings.PARLTRACK_URL + "/mep/%s?format=json&date=%s" % (mep.encode("Utf-8"), rd.date.strftime("%Y-%m-%d"))
                mep_ep_id = json.loads(urlopen(settings.PARLTRACK_URL + "/mep/%s?format=json&date=%s" % (mep.encode("Utf-8"), rd.date.strftime("%Y-%m-%d"))).read())["UserID"]
                print mep_ep_id, mep, json.loads(urlopen(settings.PARLTRACK_URL + "/mep/%s?format=json&date=%s" % (mep.encode("Utf-8"), rd.date.strftime("%Y-%m-%d"))).read())["Name"]["full"]
                representative = MEP.objects.get(ep_id=mep_ep_id).representative_ptr
                print "Create vote for", representative.first_name, representative.last_name
                Vote.objects.create(choice=choice, recommendation=r, representative=representative, name=rd.proposal_name)
                a += 1

    # clean scores before adding new one
    proposal.score_set.all().delete()

    rep_scores = {}
    for rec in proposal.recommendation_set.all():
        for vote in rec.vote_set.all():
            if vote.representative not in rep_scores.keys():
                rep_scores[vote.representative] = [0, 0]
            if vote.choice == vote.recommendation.recommendation:
                rep_scores[vote.representative][0] += vote.recommendation.weight * 2
            elif vote.choice == "abstention":
                if vote.recommendation.recommendation == "against":
                    rep_scores[vote.representative][0] += vote.recommendation.weight * 1
                elif vote.recommendation.recommendation == "for":
                    rep_scores[vote.representative][0] += vote.recommendation.weight * -1
                else:
                    raise
            elif (vote.choice == "for" and vote.recommendation.recommendation == "against") or\
                 (vote.choice == "against" and vote.recommendation.recommendation == "for"):
                rep_scores[vote.representative][0] += vote.recommendation.weight * -2
            else:
                raise
            rep_scores[vote.representative][1] += vote.recommendation.weight

    z = 1
    for i in rep_scores.keys():
        sys.stdout.write("Creating scores %i/%i\r" % (z, len(rep_scores.keys())))
        sys.stdout.flush()
        z += 1
        Score.objects.create(value=25*(float(rep_scores[i][0])/rep_scores[i][1]) + 50,
                             representative=i,
                             proposal=proposal,
                             date=rd.date)

    sys.stdout.write("\n")
    rd.imported = True
    rd.save()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >>sys.stderr, "Usage: %s <recommendationdata id> <{for,against}> <weight>" % __file__
        sys.exit(1)
    recommendationdata_id, recommendation, weight = sys.argv[1:]
    if len(check_recommendationdata(recommendationdata_id)) != 0:
        print >>sys.stderr, "I didn't managed to get all the meps :("
        sys.exit(1)
    if sys.argv[-2] not in ("for", "against"):
        print >>sys.stderr, "Recommendation should be either 'for' or 'against'"
        sys.exit(1)
    create_recommendation(*sys.argv[1:])
    sys.stdout.write("Update total score of all meps now\n")
    update_total_score_of_all_meps(verbose=True)
    sys.stdout.write("Clean all deprecated trends\n")
    clean_all_trends()

# vim:set shiftwidth=4 tabstop=4 expandtab:
