from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode
from django import template
from meps.models import Country
from reps.models import Party

register = template.Library()

@register.inclusion_tag("blocks/menu_item.html")
def menu_item(items):
    return {"objects": items}

@register.inclusion_tag("blocks/navigation.html")
def build_menu():
    return {'menus':
                [{'name': 'Country',
                  'content':
                ({"url": "country:%s" % country.code,
                  "display": country.name} for country in Country.objects.all().order_by("name"))
                  },
                 {'name': 'Party',
                  'content': ({"url": "party:%s" % party.name,
                  "display": party.name} for party in Party.objects.all().order_by("name"))},
                ]
            }


