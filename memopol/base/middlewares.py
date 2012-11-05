import logging
from email.utils import parsedate
import calendar

from django.conf import settings
from django.utils.hashcompat import md5_constructor
from django.utils.cache import patch_response_headers, patch_cache_control, get_max_age
from django.utils.encoding import iri_to_uri
from django.http import HttpResponseNotModified
from django.core.cache import get_cache

log = logging.getLogger(__name__)


class CacheControlHeaders(object):
    def __init__(self):
        self.ttl = settings.CACHE_MIDDLEWARE_SECONDS

    def process_response(self, request, response):
        """
        Very basic default cache-control management.
        Set a cache-control if None has been already set.
        TODO:
        - manage user authentication
        - manage IMS
        - manage 500
        - manage dontcache
        """

        if not response.has_header('Cache-Control'):
            # If there is no cache-control header, we are going to add one.
            # Was Last-Modified set already ?
            if response.has_header('Last-Modified'):
                # Good. patch_response_headers
                patch_cache_control(response, max_age=self.ttl)
            else:
                # Since we don't have a Last-Modified header, use
                # patch_response_headers, which will set a bunch of headers
                patch_response_headers(response)

        return response
