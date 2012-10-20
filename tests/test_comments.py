# -*- coding: utf-8 -*-
from . import TestCase, UserTestCase
from meps.models import MEP


class TestComments(TestCase):

    def test_meps_comments_required_field(self):
        """test comments"""
        resp = self.app.get(MEP.objects.all()[0].get_absolute_url())
        print resp.forms
        form = resp.forms[0]
        resp = form.submit()
        resp.mustcontain('This field is required.')

    def test_meps_comments(self):
        """test comments"""
        resp = self.app.get(MEP.objects.all()[0].get_absolute_url())
        form = resp.forms[0]
        form['comment'] = 'ACTA sucks'
        form['url'] = 'http://laquadrature.net'
        resp = form.submit()
        #from ipdb import set_trace; set_trace()
        assert resp.status_int == 302, resp
        resp = resp.follow()
        resp.mustcontain('<h1>Thank you for your contribution.</h1>')


class TestCommentsModeration(UserTestCase):

    def test_meps_comments(self):
        """test comments"""
        resp = self.app.get(MEP.objects.all()[0].get_absolute_url())
        form = resp.forms[0]

        # user dont need name and email
        form['comment'] = 'ACTA sucks'
        form['url'] = 'http://laquadrature.net'
        resp = form.submit()
        assert resp.status_int == 302, resp
        resp = resp.follow()
        resp.mustcontain('<h1>Thank you for your contribution.</h1>')

        ## login as staff user
        self.set_user(is_staff=True)
        resp = self.app.get('/admin/')
        resp.mustcontain('<a href="/admin/comments/comment/">Comments</a>')
        resp = self.app.get('/admin/comments/comment/')
        resp.mustcontain('<th><a href="', '/">garage1</a></th>')
