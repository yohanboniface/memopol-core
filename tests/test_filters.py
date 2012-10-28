# -*- coding: utf-8 -*-

from . import TestCase
from memopol.base.templatetags.memopol_tags import scolorize


class TestScolorize(TestCase):

    def test_should_return_classnames(self):
        self.assertIn(
            "scolorized",
            scolorize(5, 100),
        )

    def test_should_be_a_percentage_by_default(self):
        self.assertEqual(
            "scolorized scolorized0",
            scolorize(5),
        )

    def test_positive_result_should_not_have_a_hyphen(self):
        self.assertEqual(
            "scolorized scolorized3",
            scolorize(37, 100),
        )

    def test_negative_score_should_be_kept(self):
        self.assertEqual(
            "scolorized scolorized-0",
            scolorize(-5, 100),
        )

    def test_max_score_should_be_used_if_provided(self):
        self.assertEqual(
            "scolorized scolorized5",
            scolorize(20, 40),
        )

    def test_max_score_possible_should_be_rounded_at_10(self):
        self.assertEqual(
            "scolorized scolorized10",
            scolorize(40, 40),
        )

    def test_nearly_max_score_possible_should_be_rounded_at_9(self):
        self.assertEqual(
            "scolorized scolorized9",
            scolorize(99, 100),
        )

    def test_zero_should_be_rounded_at_0(self):
        self.assertEqual(
            "scolorized scolorized0",
            scolorize(0),
        )

    def test_should_accept_float_score(self):
        self.assertEqual(
            "scolorized scolorized2",
            scolorize(27.9),
        )

    def test_should_not_raise_if_score_is_None(self):
        self.assertEqual(
            "scolorized",
            scolorize(),
        )
