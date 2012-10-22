# -*- coding: utf-8 -*-
import logging

from django.views.generic import TemplateView

from haystack.query import SearchQuerySet, EmptySearchQuerySet

from dynamiq.utils import get_advanced_search_formset_class, FormsetQBuilder, ParsedStringQBuilder

from .forms import MEPSearchForm, MEPSearchAdvancedFormset
from .shortcuts import TopRated, WorstRated


log = logging.getLogger(__name__)


class SearchView(TemplateView):

    template_name = 'search/search.html'
    list_template_name = "blocks/representative_list.html"
    DEFAULT_SEARCH_LIMIT = 15

    def get_template_names(self):
        """
        Dispatch template according to the kind of request: ajax or normal.
        """
        if self.request.is_ajax():
            return [self.list_template_name]
        else:
            return [self.template_name]

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
            limit = self.request.GET.get("limit", self.DEFAULT_SEARCH_LIMIT)
        else:
            formset = formset_class(self.request.GET or None)
            formset.full_clean()
            if formset.is_valid():
                F = FormsetQBuilder(formset)
                query, label = F()
                sort = formset.options_form.cleaned_data.get("sort")
                limit = formset.options_form.cleaned_data.get("limit", self.DEFAULT_SEARCH_LIMIT)

        if query:
            results = SearchQuerySet().filter(query)
            if sort:
                results = results.order_by(sort)
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
            },
            "list_template_name": self.list_template_name,
            "per_page": limit
        }


class XhrSearchView(SearchView):

    template_name = "search/xhr.html"
