import re
from django import template

register = template.Library()

@register.filter
def floors_suffix(value, *args):
    value = re.sub('^0', '', value)
    if value == "1":
        return value + 'st'
    if value == "2":
        return value + 'nd'
    if value == "3":
        return value + 'rd'
    return value + 'th'
