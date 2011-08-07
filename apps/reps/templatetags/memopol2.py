from django.template import Library, Variable
from django.conf import settings
from django import template
import random

register = Library()

@register.simple_tag
def root_url():
    return settings.ROOT_URL

@register.simple_tag
def media_url():
    return settings.MEDIA_URL

@register.filter
def phone(value):
    for v in ('(0)', ' '):
        value = value.replace(v, '')
    return value

