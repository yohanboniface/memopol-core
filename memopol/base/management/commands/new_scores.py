import sys

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models  import Sum

from memopol.meps.models import MEP
from memopol.votes.models import Score, Recommendation, Vote, Proposal

class Command(BaseCommand):
    help = 'Initialize memopol2'

    def handle(self, *args, **options):
        scores = Score.objects.filter(representative__mep__isnull=False).select_related('representative', 'proposal')
        with transaction.commit_on_success():
            scores_len = scores.count()
            for number, score in enumerate(scores, 1):
                sys.stdout.write("%s/%s\r" % (number, scores_len))
                sys.stdout.flush()
                score.value = 0
                max_score_on_proposal = 0
                for recommendation in Recommendation.objects.filter(proposal=score.proposal).select_related('proposal'):
                    if recommendation.weight is None:
                        continue
                    max_score_on_proposal += recommendation.weight
                    vote = Vote.objects.get(recommendation=recommendation, representative=score.representative)
                    if vote.choice in ('for', 'against') and vote.choice == recommendation.recommendation:  # has followed our recommendation
                        score.value += 1 * recommendation.weight
                    elif vote.choice in ('for', 'against') and vote.choice != recommendation.recommendation:  # contrary
                        score.value -= 1 * recommendation.weight
                    elif vote.choice in ('absent', 'abstention'):
                        if recommendation.recommendation == "against":
                            score.value += 0.5 * recommendation.weight
                        else:
                            score.value -= 0.5 * recommendation.weight
                score.value = (recommendation.proposal.ponderation * score.value) / (max_score_on_proposal)
                score.value *= 10
                score.save()
            sys.stdout.write("\n")

            mep_count = MEP.objects.count()
            for number, mep in enumerate(MEP.objects.all(), 1):
                sys.stdout.write("%s/%s\r" % (number, mep_count))
                mep.total_score = Score.objects.filter(representative__mep=mep).aggregate(Sum('value'))['value__sum']
                mep_proposals_ponderation = Proposal.objects.filter(score__representative=mep).aggregate(Sum('ponderation'))['ponderation__sum']
                if mep_proposals_ponderation is not None:
                    mep.max_score_could_have = 10 * mep_proposals_ponderation
                mep.save()
            sys.stdout.write("\n")

            vote_count = Vote.objects.count()
            for number, vote in enumerate(Vote.objects.filter(representative__mep__isnull=False), 1):
                sys.stdout.write("%s/%s\r" % (number, vote_count))
                vote.score # dirty hack because this is a lazy property, I'm too lazy to write the actual code
            sys.stdout.write("\n")
