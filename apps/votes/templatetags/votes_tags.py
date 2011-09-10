from django import template
from votes.models import Vote

register = template.Library()

@register.simple_tag(takes_context=True)
def mep_votes_list_on_proposal(context, mep, proposal):
    context['mep_votes'] = Vote.objects.filter(representative=mep.representative_ptr, recommendation__proposal=proposal)
    return ''
