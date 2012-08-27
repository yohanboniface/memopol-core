# -*- coding: utf-8 -*-

from extended_choices import Choices

from dynamiq.forms.haystack import HaystackForm
from dynamiq.forms.base import DynamiqSearchOptionsForm, DynamiqAdvancedFormset
from dynamiq.fields import DynamiqStrChoiceField, DynamiqIntChoiceField

from .models import MEP, Country, Group, Committee, Delegation


def model_choice_value(model):
    """
    In MODEL_CHOICES, we need to add the app_label AND the model name
    """
    return '%s:%s' % (model._meta.app_label, model._meta.object_name)

COUNTRY = Choices(*((c.code.upper(), c.code, c.name) for c in Country.objects.all()))
GROUP = Choices(*((g.abbreviation.upper(), g.abbreviation, g.name) for g in Group.objects.all()))
COMMITTEE = Choices(*((c.abbreviation.upper(), c.abbreviation, c.name) for c in Committee.objects.all()))
DELEGATION = Choices(*(("DELEGATION_%d" % d.pk, d.pk, d.name) for d in Delegation.objects.all()))


FILTER_NAME = Choices(
    ('FULLTEXT', 'fulltext', u'Nom'),
    # ('ALL_TITLES', 'suptitle,title,subtitle', u'Titraille'),
    ('TITLE', 'title', u'Titre'),
    ('IS_ACTIVE', 'is_active', u'Active'),
    ('COUNTRY', 'country', u'Country'),
    ('GROUP', 'group', u'Group'),
    ('COMMITTEE', 'committees', u'Committee'),
    ('DELEGATION', 'delegations', u'Delegation'),
    ('TOTAL_SCORE', 'total_score', u'Score'),
)

SORT_CHOICES = Choices(
    # ('LAST_CREATED', '-created_at', u'Date de création'),
    # ('LAST_MODIFIED', '-modified_at', u'Date de modification'),
    ('TOTAL_SCORE', '-total_score', u'Score'),
    ('TOTAL_SCORE_ASC', 'total_score', u'Score asc'),
    # ('XXX', '-publication_date,page_number', u'Date de pub.'),
    # ('XXX', 'publication_date,page_number', u'Date de pub.'),
    # ('RELEVANCE', '-sesql_relevance', u'Pertinence'),
    # ('LAST_PUBLISHED', '-publication_date_time', u'Date de publication web'),
)

IS_ACTIVE = Choices(
    ('TRUE', True, u'Oui'),
    ('FALSE', False, u'Non'),
)

MODEL_CHOICES = Choices(
    # ('CONTENTMODELS', ','.join('libe:%s' % c for c in XXX), "Contenus"),
    ('MEP', model_choice_value(MEP), MEP._meta.verbose_name),
)


class MEPSearchOptionsForm(DynamiqSearchOptionsForm):

    SORT = SORT_CHOICES
    SORT_INITIAL = SORT.TOTAL_SCORE


class MEPSearchForm(HaystackForm):
    options_form_class = MEPSearchOptionsForm

    FILTER_NAME = FILTER_NAME

    _FILTER_TYPE_BY_NAME = {
        FILTER_NAME.FULLTEXT: 'fulltext',
        FILTER_NAME.TITLE: 'fulltext',
        FILTER_NAME.IS_ACTIVE: 'int',
        FILTER_NAME.COUNTRY: 'str',
        FILTER_NAME.GROUP: 'str',
        FILTER_NAME.COMMITTEE: 'str',
        FILTER_NAME.DELEGATION: 'int',
        FILTER_NAME.TOTAL_SCORE: 'int',
    }
    _FILTER_VALUE_RECEPTACLE_BY_NAME = {
        FILTER_NAME.FULLTEXT: 'fulltext',
        FILTER_NAME.TITLE: 'fulltext',
        FILTER_NAME.IS_ACTIVE: 'yes_no',
        FILTER_NAME.COUNTRY: 'country',
        FILTER_NAME.GROUP: 'group',
        FILTER_NAME.COMMITTEE: 'committees',
        FILTER_NAME.DELEGATION: 'delegations',
        FILTER_NAME.TOTAL_SCORE: 'int',
    }

    filter_value_country = DynamiqStrChoiceField(COUNTRY)
    filter_value_group = DynamiqStrChoiceField(GROUP)
    filter_value_committees = DynamiqStrChoiceField(COMMITTEE)
    filter_value_delegations = DynamiqIntChoiceField(DELEGATION)

    JS_FILTERS_BUILDERS = (
        (u'vider', {
            'replace': True,
            'filter_name': FILTER_NAME.FULLTEXT
        }),
        (u'actif', {
            'filter_name': FILTER_NAME.IS_ACTIVE,
            'filter_lookup': HaystackForm.FILTER_LOOKUPS_INT.EXACT,
            'filter_value': IS_ACTIVE.TRUE,
        }),
        (u'nom', {
            'filter_name': FILTER_NAME.FULLTEXT,
            'previous_right_op': HaystackForm.FILTER_RIGHT_OP.AND,
        }),
    )


class MEPSearchAdvancedFormset(DynamiqAdvancedFormset):
    options_form_class = MEPSearchOptionsForm
    form = MEPSearchForm

    def get_initial_data(self):

        initial_options = {
            'model': "MEP",
            'limit': 15,
        }
        initial = {}
        # initial = [
        #     {
        #         'filter_name': FILTER_NAME.EDITORIAL_SOURCE,
        #         'int_lookup': FILTER_LOOKUPS_INT.EXACT,
        #         'filter_value_editor_source': EDITORIAL_SOURCE_CHOICES.PRINT,
        #         'filter_right_op': FILTER_RIGHT_OP.AND,
        #     },
        # ]
        return initial, initial_options
