#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from django.http import HttpResponse

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

# This one come from pyramid
# https://github.com/Pylons/pyramid/blob/master/pyramid/decorator.py
class reify(object):

    """ Put the result of a method which uses this (non-data)
    descriptor decorator in the instance dict after the first call,
    effectively replacing the decorator with an instance variable."""

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except: # pragma: no cover
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val

