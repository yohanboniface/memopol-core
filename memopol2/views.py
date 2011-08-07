# -*- coding: utf-8 -*-
import logging
from django import forms
from django.conf import settings
from django.views.generic.simple import direct_to_template
from whoosh.filedb.filestore import FileStorage
from whoosh import index, fields
from whoosh.qparser import QueryParser
from memopol2.search import WHOOSH_SCHEMA
from memopol2.search import Searchables

from meps import models
from mps import models

log = logging.getLogger(__name__)

types_choices = sorted([(k.__name__.lower(), k.__name__) for k in Searchables.items])

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label='Search',
                        widget=forms.TextInput(attrs={'autocomplete':'off'}))
    types = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                choices=types_choices, required=False)


def search(request, template_name='search.html'):
    """
    Simple search view, which accepts search queries via url, like google.
    Use something like ?q=this+is+the+serch+term

    """
    hits = []
    data = dict(
            q = request.GET.get('q', ''),
            types = request.GET.getlist('types') or [],
        )
    form = SearchForm(data)
    form.is_valid()
    query = form.cleaned_data['q']
    types = form.cleaned_data['types']
    limit = int(request.GET.get('limit', 0)) or None
    if query not in (None, u"", u"*"):
        storage = FileStorage(settings.WHOOSH_INDEX)
        ix = storage.open_index(indexname='memopol')
        # Whoosh don't understands '+' or '-' but we can replace
        # them with 'AND' and 'NOT'.
        query = query.replace('+', ' AND ').replace(' -', ' NOT ')
        if types and len(types) != len(types_choices):
            query = 'type:(%s) %s' % (' OR '.join(types), query)
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
            try:
                hits = searcher.search(qry, limit=limit)
            except Exception, e:
                log.critical('Error while searching %s' % qry)
                log.exception(e)
        ix.close()
    return direct_to_template(request, template_name,
                              dict(form=form, hits=hits))


