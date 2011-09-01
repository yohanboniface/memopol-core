from votes.models import Proposal, Score
from django.db.models import Sum

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
