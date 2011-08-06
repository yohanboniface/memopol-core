#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.base import TemplateSyntaxError

def check_dir(filename):
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

def send_file(request, filename, content_type='text/plain'):
    """
    Send a file through Django.
    """
    buffer = open(filename, 'rb').read()
    response = HttpResponse(buffer, content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)
    return response

def get_content_cache(request, filename, content_type='image/png'):
    """
    Return the cached image if exists and refresh is not forced
    Otherwise return False
    """
    if request.GET.get(u'force', u'0') != u'0':
        return False
    if not os.path.exists(filename):
        return False
    return send_file(request, filename, content_type=content_type)

global _cache
_cache = {}

def cached(expire):
    """cache the whole response for ``expire`` delay"""
    def wrapper(func):
        def wrapped(request, **kwargs):
            global _cache
            path = '%s:%s' % (request.user.is_anonymous() and 'anon' or 'auth', request.path)
            if path in _cache:
                ctime, resp = _cache[path]
                if ctime > int(time.time()):
                    return resp
            resp = func(request, **kwargs)
            _cache[path] = (int(time.time()) + expire, resp)
            return resp
        return wrapped
    return wrapper

class snippet(property):

    dirname = os.path.join(os.path.dirname(__file__), 'templates')

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, klass):
        template = 'snippets/%s-%s-%s.html' % (klass.__name__.lower(), instance.id, self.name)
        if os.path.isfile(os.path.join(self.dirname, template)):
            return render_to_string(template)
        else:
            return 'x<!-- %s -->' % template


