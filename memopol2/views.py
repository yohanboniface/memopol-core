# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic.simple import direct_to_template
from whoosh.filedb.filestore import FileStorage
from whoosh import index, fields
from whoosh.qparser import QueryParser
from memopol2.search import WHOOSH_SCHEMA


def search(request, template_name='search.html'):
    """
    Simple search view, which accepts search queries via url, like google.
    Use something like ?q=this+is+the+serch+term

    """
    storage = FileStorage(settings.WHOOSH_INDEX)
    ix = storage.open_index(indexname='memopol')
    hits = []
    query = request.GET.get('q', None)
    if query is not None and query != u"":
        # Whoosh don't understands '+' or '-' but we can replace
        # them with 'AND' and 'NOT'.
        query = query.replace('+', ' AND ').replace(' -', ' NOT ')
        parser = QueryParser("content", schema=ix.schema)
        try:
            qry = parser.parse(query)
        except:
            # don't show the user weird errors only because we don't
            # understand the query.
            # parser.parse("") would return None
            qry = None
        if qry is not None:
            searcher = ix.searcher()
            hits = searcher.search(qry)

    return direct_to_template(request, template_name,
                              {'query': query, 'hits': hits})


