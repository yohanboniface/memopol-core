# -*- coding: utf-8 -*-
from . import TestCase
from mps.models import MP
from django.db.models import Count
from django.core.urlresolvers import reverse


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
        assert len(resp.pyquery('div#scores li')) == mp.scores.count()

    def test_mps_has_scores_display_title(self):
        mp = MP.objects.all().annotate(score_len=Count('score')).filter(score_len__gt=0)[0]
        resp = self.app.get(mp.get_absolute_url())
        assert mp.scores[0].proposal.title in resp.pyquery('div#scores div.inner-score a')[0].text

    def test_mps_has_score_display_link_to_wiki(self):
        mp = MP.objects.all().annotate(score_len=Count('score')).filter(score_len__gt=0)[0]
        resp = self.app.get(mp.get_absolute_url())
        assert resp.pyquery("div#scores div.inner-score a")[1].attrib["href"] == "http://www.laquadrature.net/wiki/" + mp.scores[0].proposal.id

    def test_mps_has_score_display_link_to_mp_votes_on_proposal(self):
        mp = MP.objects.all().annotate(score_len=Count('score')).filter(score_len__gt=0)[0]
        resp = self.app.get(mp.get_absolute_url())
        assert resp.pyquery("div#scores div.inner-score a")[0].attrib["href"] == reverse("mps:votes:votes_mp", args=[mp.scores[0].proposal.pk, mp.pk])
