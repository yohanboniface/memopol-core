# -*- coding: utf-8 -*-
import logging

from django.views.generic import TemplateView

from haystack.query import SearchQuerySet, EmptySearchQuerySet

from dynamiq.utils import get_advanced_search_formset_class, FormsetQBuilder, ParsedStringQBuilder

from .forms import MEPSearchForm, MEPSearchAdvancedFormset, MEPSimpleSearchForm
from .shortcuts import TopRated, WorstRated


log = logging.getLogger(__name__)


class SearchView(TemplateView):

    template_name = 'search/search.html'
    list_template_name = "blocks/representative_list.html"

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
        sort = MEPSearchAdvancedFormset.options_form_class.SORT_INITIAL
        limit = MEPSearchAdvancedFormset.options_form_class.LIMIT_INITIAL
        label = ""

        formset_class = get_advanced_search_formset_class(self.request.user, MEPSearchAdvancedFormset, MEPSearchForm)
        if "q" in self.request.GET:
            form = MEPSimpleSearchForm(self.request.GET)
            if form.is_valid():
                F = ParsedStringQBuilder(form.cleaned_data['q'], MEPSearchForm)
                query, label = F()
                formset = formset_class()
                _limit = form.cleaned_data.get("limit")
                if _limit is not None: limit = _limit
                sort = form.cleaned_data.get("sort") or sort
        else:
            form = MEPSimpleSearchForm()
            formset = formset_class(self.request.GET or None)
            formset.full_clean()
            if formset.is_valid():
                F = FormsetQBuilder(formset)
                query, label = F()
                sort = formset.options_form.cleaned_data.get("sort", sort)
                limit = formset.options_form.cleaned_data.get("limit", limit)

        if query:
            results = SearchQuerySet().filter(query)
            if sort:
                results = results.order_by(sort)
            if not limit:
                # When iterating over SearchQuerySet, haystack will fetch
                # results 10 by 10. This fetchs them all in one call:
                results = results[:]
			# we must find the average score for the search results
            average = sum([mep.total_score for mep in results])/len(results)
        else:
            results = EmptySearchQuerySet()
            average = 0.0
        return {
            "dynamiq": {
                "results": results,
                "label": label,
                "formset": formset,
                "form": form,
				"average": average,
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
