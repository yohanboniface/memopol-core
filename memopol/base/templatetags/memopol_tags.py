# -*- coding: utf-8 -*-

from django import template

from memopol.meps.models import Country, Group, Committee

register = template.Library()


@register.inclusion_tag("blocks/navigation.html")
def build_menu():
    return {
        'menus': [{
            'id': 'countries_menu',
            'name': 'Country',
            'content': ({
                "url": "country:%s is_active:1" % country.code,
                "display": country.name,
                "image": "/static/img/countries/small/%s.png" % country.code} for country in Country.objects.all().order_by("name")),
            'flyout_class': 'four',
        },
        {
            'id': 'groups_menu',
            'name': 'Political group',
            'content': ({
                "url": "group:%s is_active:1" % group.abbreviation,
                "display": group.name,
                "image": "/static/img/groups/eu/%s.png" % group.abbreviation.replace("/", "")} for group in Group.ordered_by_meps_count()),
            'flyout_class': 'twelve',
        },
        {
            'id': 'committees_menu',
            'name': 'Committees',
            'content': ({
                "url": "committees:%s is_active:1" % committee.abbreviation,
                "code": committee.abbreviation,
                "display": committee.name} for committee in Committee.ordered_by_meps_count()),
            'flyout_class': 'twelve',
        },
        ]
    }


@register.filter
def scolorize(score, max_score=100):
    """
    Output classnames to colorize a score in the frontend.
    If `max_score` is not given, we assum that `score` is a percentage.
    """
    classnames = "scolorized"  # A generic class, for factorizing CSS
                               # and help retrieving all the scores in js
    if score is not None:
        # No score means no specific class
        prefix = "-" if score < 0 else ""
        score = abs(score)
        percentage = 100.0 * score / max_score
        idx = percentage / 10  # use 10 ref
        classnames += " scolorized%s%s" % (prefix, int(idx))  # will output scolorized1
                                                             # or scolorized-1 if negative
    return classnames


@register.inclusion_tag("blocks/achievement.html")
def render_achievement(achievement):
    return {
        "achievement": achievement
    }
