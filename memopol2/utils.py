#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from django.http import HttpResponse

def check_dir(filename):
    if not os.path.exists("/".join(filename.split("/")[:-1])):
        for i in xrange(-3, 0):
            path = "/".join(filename.split("/")[:i])
            if not os.path.exists(path):
                os.mkdir(path)

def send_file(request, filename, content_type='text/plain'):
    """
    Send a file through Django.
    """
    ## Seems to no longer work with recent django
    #wrapper = FileWrapper(open(filename))
    buffer = open(filename, 'rb').read()
    response = HttpResponse(buffer, content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)
    return response

def get_content_cache(request, filename, content_type='image/png'):
    """
    Return the cached image if exists and reffresh is not forced
    Otherwise return False
    """
    if request.GET.get(u'force', u'0') != u'0':
        return False
    if not os.path.exists(filename):
        return False
    return send_file(request, filename, content_type=content_type)
