from dynamiq.shortcuts import SearchShortcut

from .forms import MEPSearchForm, MEPSearchOptionsForm


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
