from sys import stdout

from meps.models import MEP
from votes.models import Proposal, Score
from django.db.models import Sum

def update_total_score_of_all_meps(verbose=False, mep=MEP, score=Score, proposal=Proposal):
    if verbose:
        a, total_meps = 0, mep.objects.filter().count()
    for mep in mep.objects.all():
        if verbose:
            a += 1
            stdout.write("Calculating score of meps ... %s/%s\r" % (a, total_meps))
        stdout.flush()
        update_total_score_of_mep(mep, score=score, proposal=proposal)

    if verbose:
        stdout.write("\n")

def update_total_score_of_mep(mep, proposal=Proposal, score=Score):
    proposals = proposal.objects.all()
    total = proposal.objects.aggregate(Sum('ponderation'))['ponderation__sum']
    # all the votes a mep has been involved in
    done = [_score.proposal for _score in score.objects.filter(representative=mep.representative_ptr)]
    total_score = sum([_score.value * _score.proposal.ponderation for _score in score.objects.filter(representative=mep.representative_ptr)])
    # add 50 by default to votes a meps hasn't been involved in
    total_score += sum([50 * missing.ponderation for missing in proposals if missing not in done])
    mep.total_score = total_score / float(total)
    mep.save()
