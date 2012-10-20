# -*- coding: utf-8 -*-
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import unittest
import logging
from webtest import TestApp, TestResponse
from pyquery import PyQuery as pq
import django.core.handlers.wsgi

logging.getLogger('django.db.backends').setLevel(logging.WARN)
log = logging.getLogger('nose')

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH + "/memopol2")
sys.path.append(BASE_PATH)
import settings

settings.DEBUG_PROPAGATE_EXCEPTIONS = True
settings.MIDDLEWARE_CLASSES += ('django.contrib.auth.middleware.RemoteUserMiddleware',)
settings.AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
)
settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

from django.core import mail
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

django_app = django.core.handlers.wsgi.WSGIHandler()


class TestCase(unittest.TestCase):

    visited = set()

    def setUp(self):
        mail.outbox = []
        self.app = TestApp(django_app)

    def visit_links(self, links):
        links = set([pq(a).attr.href for a in links])
        for l in links:
            if isinstance(l, unicode):
                l = l.encode('utf-8')
            if l not in self.visited:
                self.visited.add(l)
                try:
                    self.app.get(l)
                    log.debug('visiting %r', l)
                except Exception:
                    log.warn('seems that %r is not a valid url. cant be encoded', l)

    @property
    def mails(self):
        out = []
        for m in mail.outbox:
            r = TestResponse()
            r.content_type = 'text/email'
            r.unicode_body = u'From: %s\nTo: %s\nSubject: %s\n\n%s' % (m.from_email, ', '.join(m.to), m.subject, m.body)
            out.append(r)
        return out

    @property
    def mail(self):
        return self.mails[0]


class UserTestCase(TestCase):

    user = None
    user_data = dict(id=99, username='garage1', email='garage@lqdn.fr')

    def setUp(self):
        mail.outbox = []
        self.set_user()

    def set_anonymous(self):
        self.app = TestApp(django_app)

    def set_user(self, **kwargs):
        user, created = User.objects.get_or_create(**self.user_data)
        user.set_password('passwd')
        for k, v in kwargs.items():
            setattr(user, k, v)
        if 'is_staff' in kwargs:
            # staff is allowed to edit comments
            ctype = ContentType.objects.get(name='comment')
            perms = Permission.objects.filter(content_type=ctype)
            user.user_permissions = perms
        else:
            user.user_permissions = []
        user.save()
        self.app = TestApp(django_app, extra_environ={'REMOTE_USER': str(user.username)})
        self.user = user
        return user

    def tearDown(self):
        self.user.delete()
