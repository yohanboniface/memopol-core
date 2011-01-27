from django.http import Http404
from couchdbkit.exceptions import ResourceNotFound

def get_couch_doc_or_404(klass, key):
    try:
        return klass.get(key)
    except ResourceNotFound:
        raise Http404


class TestFailure(Exception):
    """ for simulated failures
    """
    pass
