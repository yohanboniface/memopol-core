# -*- coding: utf-8 -*-
import logging

from django.views.generic import TemplateView
from django.db.models import Q

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
        if "fulltext" in self.request.GET:
            form = MEPSimpleSearchForm(self.request.GET)
            formset = formset_class()
            if form.is_valid():
                query = self.build_simple_search_query(form)
                limit = form.options_form.cleaned_data.get("limit") or limit
                sort = form.options_form.cleaned_data.get("sort") or sort
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
            print "sort", sort
            if sort:
                results = results.order_by(sort)
        else:
            results = EmptySearchQuerySet()

        return {
            "dynamiq": {
                "results": results,
                "label": label,
                "formset": formset,
                "form": form,
                "shortcuts": [
                    TopRated({"request": self.request}),
                    WorstRated({"request": self.request})
                ]
            },
            "list_template_name": self.list_template_name,
            "per_page": limit
        }

    def build_simple_search_query(self, form):
        """
        Generate a Q object from a simple form.
        """
        query = Q()
        for field_name, field in form.fields.items():
            value = form.cleaned_data.get(field_name)
            if value != "":
                filter_type = MEPSearchForm.determine_filter_type(field_name)
                filter_lookup = MEPSearchForm.FILTER_LOOKUPS[filter_type]
                query &= Q(**{'%s__%s' % (field_name, filter_lookup): value})
        return query


class XhrSearchView(SearchView):

    template_name = "search/xhr.html"
