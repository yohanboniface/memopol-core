from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode
from django import template

register = template.Library()


@register.simple_tag
def simple_search_shortcut(search_string):
    """
    Return a simple search URL from a search string, like "daniel OR country:CZ".
    """
    base_url = reverse("search")
    return "%s?q=%s" % (base_url, urlencode(search_string))
