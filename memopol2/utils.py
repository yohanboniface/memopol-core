#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template.base import TemplateSyntaxError
from django.conf import settings
from django.core.cache import cache

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

# Code taken in dingus to fix south migration loading fixtures
# https://github.com/garybernhardt/dingus/blob/master/dingus.py

from functools import wraps

def patch(object_path, new_object):
    module_name, attribute_name = object_path.rsplit('.', 1)
    return _Patcher(module_name, attribute_name, new_object)

def _dot_lookup(thing, comp, import_path):
    try:
        return getattr(thing, comp)
    except AttributeError:
        __import__(import_path)
        return getattr(thing, comp)

def _importer(target):
    components = target.split('.')
    import_path = components.pop(0)
    thing = __import__(import_path)

    for comp in components:
        import_path += ".%s" % comp
        thing = _dot_lookup(thing, comp, import_path)
    return thing

class _Patcher:
    def __init__(self, module_name, attribute_name, new_object):
        self.module_name = module_name
        self.attribute_name = attribute_name
        self.module = _importer(self.module_name)
        self.new_object = new_object

    def __call__(self, fn):
        @wraps(fn)
        def new_fn(*args, **kwargs):
            self.patch_object()
            try:
                return fn(*args, **kwargs)
            finally:
                self.restore_object()
        return new_fn

    def __enter__(self):
        self.patch_object()

    def __exit__(self, exc_type, exc_value, traceback):
        self.restore_object()

    def patch_object(self):
        self.original_object = getattr(self.module, self.attribute_name)
        setattr(self.module, self.attribute_name, self.new_object)

    def restore_object(self):
        setattr(self.module, self.attribute_name, self.original_object)

def loaddata(orm, fixture_name):
        _get_model = lambda model_identifier: orm[model_identifier]

        with patch('django.core.serializers.python._get_model', _get_model):
            from django.core.management import call_command
            call_command("loaddata", fixture_name)

# end of code from dingus and more http://stackoverflow.com/questions/5472925/django-loading-data-from-fixture-after-backward-migration-loaddata-is-using-mod/5906258#5906258

class snippet(property):

    dirname = os.path.join(os.path.dirname(__file__), 'templates')

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, klass):
        name = klass.__name__.lower()
        key = '%s-%s-%s' % (name, self.name, instance.id)
        value = cache.get(key)
        if not value:
            template = '%ss/snippets/%s.html' % (klass.__name__.lower(), self.name)
            if name == 'mep':
                ctx = dict(instance=instance,
                           country=instance.countrymep_set.latest('end').country,
                           group=instance.groupmep_set.latest('end').group,
                           MEDIA_URL=settings.MEDIA_URL)
            elif name == 'mp':
                ctx = dict(instance=instance,
                           group=instance.group,
                           MEDIA_URL=settings.MEDIA_URL)
            value = render_to_string(template, ctx)
            cache.set(key, value, settings.SNIPPETS_CACHE_DELAY)
            print key
        return value


