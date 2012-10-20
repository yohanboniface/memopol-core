from . import TestCase
from django.db.models import Count
from django.core.urlresolvers import reverse
from mps.models import MP


class TestMPsVotes(TestCase):

    def test_page_load(self):
        mp = MP.objects.all().annotate(score_len=Count('score')).filter(score_len__gt=0)[0]
        self.app.get(reverse("mps:votes:votes_mp", args=[mp.scores[0].proposal.pk, mp.pk]))
