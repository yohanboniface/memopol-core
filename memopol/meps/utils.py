from sys import stdout

from django.db.models import Sum
from django.db import transaction

from memopol.meps.models import MEP
from memopol.votes.models import Proposal, Score


def update_total_score_of_all_meps(verbose=False, mep=MEP, score=Score, proposal=Proposal):
    if verbose:
        a, total_meps = 0, mep.objects.filter().count()
    with transaction.commit_on_success():
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
    if not done:
        mep.total_score = None
        mep.save()
        return
    total_score = sum([_score.value * _score.proposal.ponderation for _score in score.objects.filter(representative=mep.representative_ptr)])
    # add 50 by default to votes a meps hasn't been involved in
    total_score += sum([50 * missing.ponderation for missing in proposals if missing not in done])
    mep.total_score = total_score / float(total)
    mep.save()

def update_meps_positions(verbose=False, mep=MEP):
    if verbose:
        a, total_meps = 0, mep.objects.filter(active=True).count()
    previous_score = None
    position = 0
    with transaction.commit_on_success():
        for _mep in mep.objects.filter(active=True).order_by('-total_score'):
            a += 1
            # else, scores are equal -> same position
            if not _mep.total_score:
                pass
            if previous_score != _mep.total_score:
                position += 1
            if verbose:
                stdout.write("Setting current position of meps ... %s/%s\r" % (a, total_meps))
            stdout.flush()
            _mep.position = position
            _mep.save()
            previous_score = _mep.total_score

    if verbose:
        stdout.write("\n")
