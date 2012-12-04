from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode
from django import template

from dynamiq.utils import get_advanced_search_formset_class

from ..forms import MEPSearchForm, MEPSearchAdvancedFormset, MEPSimpleSearchForm

register = template.Library()


@register.simple_tag
def simple_search_shortcut(search_string, sort=None):
    """
    Return a simple search URL from a search string, like "daniel OR country:CZ".
    """
    base_url = reverse("search")
    query_string = "q=%s" % urlencode(search_string)
    if sort:
        query_string = "%s&sort=%s" % (query_string, sort)
    return "%s?%s" % (base_url, query_string)


@register.inclusion_tag('blocks/search_formset.html', takes_context=True)
def render_search_formset(context):
    """
    Display the search form, if a `dynamiq` key is on the context, it will be
    used, otherwise, it create an empty form
    """
    if 'dynamiq' in context:
        dynamiq = context['dynamiq']
    else:
        request = context['request']
        formset_class = get_advanced_search_formset_class(request.user, MEPSearchAdvancedFormset, MEPSearchForm)
        formset = formset_class(None)
        dynamiq = {
                "q": "",
                "label": "",
                "formset": formset,
            }
    return {
        'dynamiq': dynamiq
    }


@register.inclusion_tag('blocks/search_form.html', takes_context=True)
def render_search_form(context):
    """
    Display the search form, if a `dynamiq` key is on the context, it will be
    used, otherwise, it create an empty form
    """
    if 'dynamiq' in context:
        dynamiq = context['dynamiq']
    else:
        form = MEPSimpleSearchForm(None)
        dynamiq = {
                "q": "",
                "label": "",
                "form": form,
            }
    return {
        'dynamiq': dynamiq
    }
