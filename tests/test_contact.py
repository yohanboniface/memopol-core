# -*- coding: utf-8 -*-
from . import TestCase

class TestContact(TestCase):

    def test_contact(self):
        """test comments"""
        resp = self.app.get('/contact/')
        form = resp.forms['contact']
        form['name'] = 'Un Garage'
        form['email'] = 'garage@lqdn.fr'
        resp = form.submit()
        resp.mustcontain('<li>This field is required.</li>')

        form = resp.forms['contact']
        form['body'] = 'ACTA sucks'
        resp = form.submit()

        self.mail.mustcontain(
            'From: memopol@lqdn.fr',
            'To: contact@lqdn.fr',
            'Subject: [Memopol Contact] from Un Garage',
            'Un Garage - garage@lqdn.fr',
            '==========',
            'ACTA sucks',
            )
