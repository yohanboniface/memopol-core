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
                "sprite": "sprite-country_small-%s" % country.code} for country in Country.objects.all().order_by("name")),
            'flyout_class': 'four',
        },
        {
            'id': 'groups_menu',
            'name': 'Political group',
            'content': ({
                "url": "group:%s is_active:1" % group.abbreviation,
                "display": group.name,
                "sprite": "sprite-eu_group-%s" % group.abbreviation.replace("/", "")} for group in Group.ordered_by_meps_count()),
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


@register.filter
def mep_score_scolorize(mep):
    """
    Output classnames to colorize a score in the frontend.
    If `max_score` is not given, we assum that `score` is a percentage.
    """
    classnames = "scolorized"  # A generic class, for factorizing CSS
                               # and help retrieving all the scores in js
    if mep.total_score is not None:
        idx = ((mep.total_score + mep.max_score_could_have) / (mep.max_score_could_have*2)) * 10
        classnames += " scolorized%s" % int(idx)  # will output scolorized1
                                                  # or scolorized-1 if negative
    return classnames


@register.filter
def proposal_score_scolorize(score):
    """
    Output classnames to colorize a score in the frontend.
    If `max_score` is not given, we assum that `score` is a percentage.
    """
    classnames = "scolorized"  # A generic class, for factorizing CSS
                               # and help retrieving all the scores in js
    idx = (float(score.value + score.proposal.total_score) / (score.proposal.total_score*2)) * 10
    classnames += " scolorized%s" % int(idx)  # will output scolorized1
                                              # or scolorized-1 if negative
    return classnames


@register.filter
def scolorize_position(position, recommandation="for"):
    """
    Colorize a position on a vote according to a recommandation.
    Choices are "for", "against", "absent", "abstention".
    """
    if position == recommandation:
        score = 1
    elif position in ("absent", "abstention"):
        score = 0.5
    else:
        score = 0
    return scolorize(score, max_score=1)


@register.inclusion_tag("blocks/achievement.html")
def render_achievement(achievement):
    return {
        "achievement": achievement
    }


@register.inclusion_tag("blocks/call_now.html")
def call_now(phone_number):
    return {
        "phone_number": phone_number
    }
