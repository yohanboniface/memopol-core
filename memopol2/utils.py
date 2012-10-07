#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from django.http import HttpResponse
from django.core.management import call_command
from django.core.cache import cache
from django.core.servers.basehttp import FileWrapper

def get_or_create(klass, _id=None, **kwargs):
    if _id is None:
        object = klass.objects.filter(**kwargs)
    else:
        object = klass.objects.filter(**{_id : kwargs[_id]})
    if object:
        return object[0]
    else:
        print "     add new", klass.__name__, kwargs
        return klass.objects.create(**kwargs)

def update_search_index():
    call_command("update_memopol_index")

def check_dir(filename):
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

def send_file(request, filename, content_type='text/plain'):
    """
    Send a file through Django.
    """
    buffer = FileWrapper(file(filename))
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

COLORS =\
((208, 0, 0),
(222, 79, 17),
(246, 183, 36),
(253, 220, 11),
(253, 247, 11),
(232, 253, 11),
(162, 253, 11),
(114, 220, 44),
(58, 198, 9),
(55, 157, 0),
(55, 157, 0))

def color(score):
    return COLORS[int(score/10)]

def cached(expire):
    """cache the whole response for ``expire`` delay"""
    def wrapper(func):
        def wrapped(request, **kwargs):
            user = 'anon' if request.user.is_anonymous() else 'auth'
            path = '%s:%s' % (user, request.path)
            content = cache.get(path)
            if content is None:
                resp = func(request, **kwargs)
                if not resp.is_rendered:
                    resp.render()
                content = resp.content.replace('   ', '')
                cache.set(path, content, timeout=expire)
                resp = HttpResponse(content)
                resp['X-Cached'] = '0'
            else:
                resp = HttpResponse(content)
                resp['X-Cached'] = '1'
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
