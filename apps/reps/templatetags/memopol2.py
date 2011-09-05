from django.template import Library, Variable, Node, resolve_variable, TemplateSyntaxError
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

class AddParameter(Node):
  def __init__(self, varname, value):
    self.varname = varname
    self.value = value

  def render(self, context):
    req = resolve_variable('request',context)
    params = req.GET.copy()
    params[self.varname] = self.value
    return '%s?%s' % (req.path, params.urlencode())

def addurlparameter(parser, token):
  from re import split
  bits = split(r'\s+', token.contents, 2)
  if len(bits) < 2:
    raise TemplateSyntaxError, "'%s' tag requires two arguments" % bits[0]
  return AddParameter(bits[1],bits[2])

register.tag('addurlparameter', addurlparameter)
