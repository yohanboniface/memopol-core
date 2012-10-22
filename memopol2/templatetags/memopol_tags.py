from django import template
from meps.models import Country, Group

register = template.Library()


@register.inclusion_tag("blocks/navigation.html")
def build_menu():
    return {
        'menus': [{
            'name': 'Country',
            'content': ({
                "url": "country:%s" % country.code,
                "display": country.name} for country in Country.objects.all().order_by("name")),
            'flyout_class': 'four',
        },
        {
            'name': 'Political group',
            'content': ({
                "url": "group:%s" % group.abbreviation,
                "display": group.name} for group in Group.objects.all().order_by("abbreviation")),
            'flyout_class': 'twelve',
        },
        ]
    }
