# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

from extended_choices import Choices

from dynamiq.forms.haystack import HaystackForm
from dynamiq.forms.constants import YES_NO
from dynamiq.forms.base import SearchOptionsForm, AdvancedFormset
from dynamiq.fields import StrChoiceField, IntChoiceField
from dynamiq.utils import model_choice_value

from memopol.meps.models import MEP, Country, Group, Committee, Delegation, Building


COUNTRY = Choices(*((c.code.upper(), c.code, c.name) for c in Country.objects.all()))
GROUP = Choices(*((g.abbreviation.upper(), g.abbreviation, g.name) for g in Group.objects.all()))
COMMITTEE = Choices(*((c.abbreviation.upper(), c.abbreviation, c.name) for c in Committee.objects.all()))
DELEGATION = Choices(*(("DELEGATION_%d" % d.pk, d.pk, d.name) for d in Delegation.objects.all()))
# FIXME: when using django representatives, remove hardcoded postcode (use manager)
BXL_BUILDING = Choices(*((b.pk.upper(), b.pk, b.name) for b in Building.objects.filter(postcode="1047")))
STG_BUILDING = Choices(*((b.pk.upper(), b.pk, b.name) for b in Building.objects.exclude(postcode="1047")))


FILTER_NAME = Choices(
    ('FULLTEXT', 'fulltext', u'Name'),
    ('IS_ACTIVE', 'is_active', u'Active'),
    ('COUNTRY', 'country', u'Country'),
    ('GROUP', 'group', u'Group'),
    ('COMMITTEE', 'committees', u'Committee'),
    ('DELEGATION', 'delegations', u'Delegation'),
    ('TOTAL_SCORE', 'total_score', u'Score'),
    ('ACHIEVEMENT', 'achievements', u'Achievement'),
    ('BXL_BUILDING', 'bxl_building', u'Brussels building'),
    ('BXL_FLOOR', 'bxl_floor', u'Brussels floor'),
    ('STG_BUILDING', 'stg_building', u'Strasbourg building'),
    ('STG_FLOOR', 'stg_floor', u'Strasbourg floor'),
)

SORT_CHOICES = Choices(
    ('LAST_NAME', 'last_name', u'Sort by last name'),
    ('LAST_NAME_DESC', '-last_name', u'Sort by last name desc'),
    ('TOTAL_SCORE', '-total_score', u'Sort by score'),
    ('TOTAL_SCORE_ASC', 'total_score', u'Sort by score asc'),
)

MODEL_CHOICES = Choices(
    ('MEP', model_choice_value(MEP), MEP._meta.verbose_name),
)


class MEPSearchOptionsForm(SearchOptionsForm):

    SORT = SORT_CHOICES
    SORT_INITIAL = SORT.LAST_NAME
    LIMIT_INITIAL = 30

    limit = forms.IntegerField(
                min_value=0,
                max_value=100,
                required=True,
                initial=30,
                label=_("Total results")
            )


class MEPSearchForm(HaystackForm):
    options_form_class = MEPSearchOptionsForm

    FILTER_NAME = FILTER_NAME

    _FILTERS_BY_FIELD = {
        FILTER_NAME.FULLTEXT: {
            'type': 'fulltext',
            'receptacle': 'fulltext'
        },
        FILTER_NAME.IS_ACTIVE: {
            'type': 'yes_no',
            'receptacle': 'yes_no',
        },
        FILTER_NAME.COUNTRY: {
            'type': 'str',
            'receptacle': 'country',
        },
        FILTER_NAME.GROUP: {
            'type': 'str',
            'receptacle': 'group',
        },
        FILTER_NAME.COMMITTEE: {
            'type': 'str',
            'receptacle': 'committees',
        },
        FILTER_NAME.DELEGATION: {
            'type': 'id',
            'receptacle': 'delegations',
        },
        FILTER_NAME.TOTAL_SCORE: {
            'type': 'int',
            'receptacle': 'int',
        },
        FILTER_NAME.ACHIEVEMENT: {
            'type': 'id',
            'receptacle': 'autocomplete',
            'autocomplete_lookup': 'mep_achievements',
        },
        FILTER_NAME.BXL_BUILDING: {
            'type': 'str',
            'receptacle': 'bxl_building',
        },
        FILTER_NAME.BXL_FLOOR: {
            'type': 'str',
            'receptacle': 'str',
        },
        FILTER_NAME.STG_BUILDING: {
            'type': 'str',
            'receptacle': 'stg_building',
        },
        FILTER_NAME.STG_FLOOR: {
            'type': 'str',
            'receptacle': 'str',
        },
    }

    filter_value_country = StrChoiceField(COUNTRY)
    filter_value_group = StrChoiceField(GROUP)
    filter_value_committees = StrChoiceField(COMMITTEE)
    filter_value_delegations = IntChoiceField(DELEGATION)
    filter_value_bxl_building = StrChoiceField(BXL_BUILDING)
    filter_value_stg_building = StrChoiceField(STG_BUILDING)

    JS_FILTERS_BUILDERS = (
        (u'reset', {
            'replace': True,
            'filter_name': FILTER_NAME.FULLTEXT
        }),
        (u'active', {
            'filter_name': FILTER_NAME.IS_ACTIVE,
            'filter_lookup': HaystackForm.FILTER_LOOKUPS_INT.EXACT,
            'filter_value': YES_NO.YES,
        }),
        (u'name', {
            'filter_name': FILTER_NAME.FULLTEXT,
            'previous_right_op': HaystackForm.FILTER_RIGHT_OP.AND,
        }),
    )


class MEPSearchAdvancedFormset(AdvancedFormset):
    options_form_class = MEPSearchOptionsForm
    form = MEPSearchForm

    def get_initial_data(self):

        initial_options = {
            'model': "MEP",
            'limit': 15,
        }
        initial = [
                {
                    'filter_name': FILTER_NAME.IS_ACTIVE,
                    'yes_no_lookup': HaystackForm.FILTER_LOOKUPS_YES_NO.EXACT,
                    'filter_value_yes_no': YES_NO.YES,
                    'filter_right_op': HaystackForm.FILTER_RIGHT_OP.AND,
                },
        ]
        return initial, initial_options


class MEPSimpleSearchForm(forms.Form):

    limit = forms.IntegerField(
                min_value=0,
                max_value=100,
                required=False,
                initial=15,
                label=_("Total results")
            )
    sort = forms.ChoiceField(
                required=False,
                initial=SORT_CHOICES.LAST_NAME,
                label=_("Sort by"),
                choices=SORT_CHOICES
            )
    q = forms.CharField(
                required=False,
            )
