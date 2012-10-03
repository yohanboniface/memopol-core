# -*- coding: utf-8 -*-
import logging

from django.views.generic import TemplateView

from haystack.query import SearchQuerySet, EmptySearchQuerySet

from dynamiq.utils import get_advanced_search_formset_class, FormsetQBuilder, ParsedStringQBuilder
from dynamiq.shortcuts import SearchShortcut

from .forms import (MEPSearchForm, MEPSearchAdvancedFormset,
                    MEPSearchOptionsForm)


log = logging.getLogger(__name__)


class MEPBaseShortcut(SearchShortcut):
    base_url_name = "search"


class TopRated(MEPBaseShortcut):
    title = u"Top rated"

    def __init__(self, request):
        super(TopRated, self).__init__(request)
        self.options = {
            'sort': MEPSearchOptionsForm.SORT.TOTAL_SCORE,
            'limit': 15,
        }
        self.filters = [
            {
                'filter_name': 'total_score',
                'int_lookup': MEPSearchForm.FILTER_LOOKUPS_INT.GTE,
                'filter_value_int': 50,
                'filter_right_op': MEPSearchForm.FILTER_RIGHT_OP.EMPTY
            },
        ]


class WorstRated(MEPBaseShortcut):
    title = u"Worst rated"

    def __init__(self, request):
        super(WorstRated, self).__init__(request)
        self.options = {
            'sort': MEPSearchOptionsForm.SORT.TOTAL_SCORE_ASC,
            'limit': 15,
        }
        self.filters = [
            {
                'filter_name': 'total_score',
                'int_lookup': MEPSearchForm.FILTER_LOOKUPS_INT.GTE,
                'filter_value_int': 1,
                'filter_right_op': MEPSearchForm.FILTER_RIGHT_OP.EMPTY
            },
        ]


class SearchView(TemplateView):

    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        query = None
        sort = None
        limit = None
        label = ""
        q = ""

        formset_class = get_advanced_search_formset_class(self.request.user, MEPSearchAdvancedFormset, MEPSearchForm)
        if "q" in self.request.GET:
            q = self.request.GET['q']
            F = ParsedStringQBuilder(q, MEPSearchForm)
            query, label = F()
            formset = formset_class()
        else:
            formset = formset_class(self.request.GET or None)
            formset.full_clean()
            if formset.is_valid():
                F = FormsetQBuilder(formset)
                query, label = F()
                sort = formset.options_form.cleaned_data.get("sort")
                limit = formset.options_form.cleaned_data.get("limit", 15)

        if query:
            results = SearchQuerySet().filter(query)
            if sort:
                results = results.order_by(sort)
            if limit:
                results = results[:limit]
        else:
            results = EmptySearchQuerySet()
        return {
            "dynamiq": {
                "results": results,
                "q": q,
                "label": label,
                "formset": formset,
                "shortcuts": [
                    TopRated({"request": self.request}),
                    WorstRated({"request": self.request})
                ]
            }
        }


class XhrSearchView(SearchView):

    template_name = "search/xhr.html"
