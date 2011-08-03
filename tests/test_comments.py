# -*- coding: utf-8 -*-
from tests import *

class TestComments(TestCase):

    def test_meps_comments(self):
        """test 10 first meps"""
        resp = self.app.get('/europe/parliament/names/')
        l = pq(resp.pyquery('a[href^="/europe/parliament/deputy/"]')[0]).attr.href
        resp = self.app.get(l)
        self.assert_(len(resp.forms)==1, resp.forms)
        form = resp.form # comment form is the only one
        resp = form.submit()
        resp.mustcontain('This field is required.')

        form['name'] = 'Un Garage'
        form['email'] = 'garage@lqdn.fr'
        form['comment'] = 'ACTA sucks'
        resp = form.submit()
        assert resp.status_int == 302, resp
        resp = resp.follow()
        resp.mustcontain('<h1>Thank you for your comment.</h1>')

