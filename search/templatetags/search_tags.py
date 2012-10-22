from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode
from django import template

from dynamiq.utils import get_advanced_search_formset_class

from ..forms import MEPSearchForm, MEPSearchAdvancedFormset

register = template.Library()


@register.simple_tag
def simple_search_shortcut(search_string):
    """
    Return a simple search URL from a search string, like "daniel OR country:CZ".
    """
    base_url = reverse("search")
    return "%s?q=%s" % (base_url, urlencode(search_string))


@register.inclusion_tag('blocks/search_form.html', takes_context=True)
def render_search_form(context):
    """
    Display the search form, if a `dynamiq` key is on the context, it will
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
