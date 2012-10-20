# -*- coding: utf-8 -*-
from . import TestCase


class TestMisc(TestCase):

    def test_home_links(self):
        """test all home links like a monkey"""
        resp = self.app.get('/')
        resp.mustcontain('<h1 class="document-title">MEPs by country</h1>')
        self.visit_links(resp.pyquery('#nav a'))

    def test_meps_deputies(self):
        """test 10 first meps"""
        resp = self.app.get('/europe/parliament/names/')
        links = resp.pyquery('a[href^="/europe/parliament/deputy/"]')
        self.assert_(len(links) > 1, links)
        self.visit_links(links[:10])
