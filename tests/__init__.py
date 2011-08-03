# -*- coding: utf-8 -*-
import os
import unittest
import logging
from webtest import TestApp
from pyquery import PyQuery as pq
import django.core.handlers.wsgi

logging.getLogger('django.db.backends').setLevel(logging.WARN)
log = logging.getLogger('nose')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

django_app = django.core.handlers.wsgi.WSGIHandler()

class TestCase(unittest.TestCase):

    visited = set()

    def setUp(self):
        self.app = TestApp(django_app)

    def visit_links(self, links):
        links = set([pq(a).attr.href for a in links])
        for l in links:
            if isinstance(l, unicode):
                l = l.encode('utf-8')
            if l not in self.visited:
                self.visited.add(l)
                try:
                    resp = self.app.get(l)
                    log.debug('visiting %r', l)
                except Exception, e:
                    log.warn('seems that %r is not a valid url. cant be encoded', l) 
