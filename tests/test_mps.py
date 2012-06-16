# -*- coding: utf-8 -*-
from tests import TestCase
from mps.models import MP
from django.db.models import Count

class TestMPs(TestCase):

    def test_mps_has_scores_div(self):
        mp = MP.objects.all().annotate(score_len=Count('score')).filter(score_len__gt=0)[0]
        resp = self.app.get(mp.get_absolute_url())
        assert resp.pyquery('div#scores')

    def test_mps_doesnt_have_scores_div(self):
        mp = MP.objects.all().annotate(score_len=Count('score')).filter(score_len__exact=0)[0]
        resp = self.app.get(mp.get_absolute_url())
        assert not resp.pyquery('div#scores')

    def test_mps_has_scores_average(self):
        mp = MP.objects.all().annotate(score_len=Count('score')).filter(score_len__gt=0)[0]
        resp = self.app.get(mp.get_absolute_url())
        resp.mustcontain('Moyenne des scores : ' + str(int(mp.total_score())))

    def test_mps_has_scores_display_all(self):
        mp = MP.objects.all().annotate(score_len=Count('score')).filter(score_len__gt=0)[0]
        resp = self.app.get(mp.get_absolute_url())
        assert len(resp.pyquery('div#scores li')) == mp.scores().count()
