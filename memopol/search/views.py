# -*- coding: utf-8 -*-
import logging
import csv

from django.views.generic import TemplateView
from django.http import HttpResponse

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
            "per_page": limit,
            "as_csv":  self.request.GET.get('as_csv', False)
        }

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('as_csv', False):
            return self.render_to_csv(context, **response_kwargs)
        return super(SearchView, self).render_to_response(context,
                                                          **response_kwargs)

    def render_to_csv(self, context, **response_kwargs):
        params = self.request.GET
        response = HttpResponse(mimetype='text/csv')
        name = self.request.path.strip('/').replace('/', '_')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % name

        header = [
            'name',
            'gender',
            'score',
            'emails',
            'country',
            'group',
            'bxl building id',
            'bxl building name',
            'bxl floor',
            'bxl office number',
            'bxl fax',
            'bxl phone1',
            'bxl phone2',
            'stg building id',
            'stg building name',
            'stg floor',
            'stg office number',
            'stg fax',
            'stg phone1',
            'stg phone2',
        ]

        meps = []

        if 'object' in context:
            obj = context['object']
            meps = getattr(obj, 'meps', [])

            if hasattr(meps, 'query'):
                # got a queryset
                meps = meps.select_related().distinct()
                if 'group' in params:
                    meps = meps.filter(groups__abbreviation=params['group'])
                    if 'country' in params:
                        meps = meps.filter(countries__name=params['country'])

        delim = ','
        if 'delim' in self.request.GET:
            delim = self.request.GET['delim'].encode()
        quote = '"'
        if 'quote' in self.request.GET:
            quote = self.request.GET['quote'].encode()

        writer = csv.writer(response, delimiter=delim,
                            quotechar=quote,
                            doublequote=True)
        writer.writerow(header)

        data = self.get_context_data(**response_kwargs)

        for result in data['dynamiq']['results']:
            mep = result.object
            row = [
                unicode(mep),
                mep.gender,
                int(mep.total_score) if mep.total_score else '',
                u' - '.join(mep.emails),
                mep.country.name,
                mep.group.abbreviation,
                mep.bxl_building.id if mep.bxl_building else '',
                mep.bxl_building.name if mep.bxl_building else '',
                mep.bxl_floor,
                mep.bxl_office_number,
                mep.bxl_fax,
                mep.bxl_phone1,
                mep.bxl_phone2,
                mep.stg_building.id if mep.stg_building else '',
                mep.stg_building.name if mep.stg_building else '',
                mep.stg_floor,
                mep.stg_office_number,
                mep.stg_fax,
                mep.stg_phone1,
                mep.stg_phone2,
            ]
            str_row = []
            for v in row:
                if isinstance(v, unicode):
                    v = v.encode('utf-8')
                str_row.append(v)

            mep_committees = {}
            # FIXME: this should use current_committees but it look like its broken
            # or no longer valid
            roles = mep.committeerole_set.all()
            for role in roles:
                abbr = role.committee.abbreviation
                mep_committees.setdefault(abbr, set([])).add(role.role)
            # for c in committees:
            #     str_row.append(' - '.join(sorted(mep_committees.get(c, []))))

            assert len(str_row) == len(header)
            writer.writerow(str_row)

        return response

class XhrSearchView(SearchView):

    template_name = "search/xhr.html"
