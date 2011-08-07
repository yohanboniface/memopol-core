# -*- coding: utf-8 -*-
from tests import *
from uuid import uuid4

class TestComments(TestCase):

    def test_meps_comments(self):
        """test comments"""
        resp = self.app.get('/europe/parliament/names/')
        l = pq(resp.pyquery('a[href^="/europe/parliament/deputy/"]')[0]).attr.href
        resp = self.app.get(l)
        form = resp.forms[1]
        resp = form.submit()
        resp.mustcontain('This field is required.')

        form['name'] = 'Un Garage'
        form['email'] = 'garage@lqdn.fr'
        form['comment'] = 'ACTA sucks'
        resp = form.submit()
        assert resp.status_int == 302, resp
        resp = resp.follow()
        resp.mustcontain('<h1>Thank you for your comment.</h1>')

class TestCommentsModeration(UserTestCase):

    def test_meps_comments(self):
        """test comments"""
        resp = self.app.get('/europe/parliament/names/')
        l = pq(resp.pyquery('a[href^="/europe/parliament/deputy/"]')[0]).attr.href
        resp = self.app.get(l)
        form = resp.forms[1]

        # user dont need name and email
        form['comment'] = 'ACTA sucks'
        resp = form.submit()
        assert resp.status_int == 302, resp
        resp = resp.follow()
        resp.mustcontain('<h1>Thank you for your comment.</h1>')

        # login as staff user
        self.set_user(is_staff=True)
        resp = self.app.get('/admin/')
        resp.mustcontain('<a href="comments/comment/">Comments</a>')
        resp = self.app.get('/admin/comments/comment/')
        resp.mustcontain('<th><a href="','/">garage1</a></th>')

