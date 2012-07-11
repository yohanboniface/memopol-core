import re
from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@stringfilter
@register.filter
def floors_suffix(value, *args):
    value = re.sub('^[MT0]+', '', value)
    if value == "1":
        return value + 'st'
    if value == "2":
        return value + 'nd'
    if value == "3":
        return value + 'rd'
    return value + 'th'
