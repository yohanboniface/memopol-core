from memopol.meps.models import MEP
from django import template

register = template.Library()


@register.assignment_tag
def meps_the_assistant_is_also_working_for(assistant, mep):
    return MEP.objects.filter(assistantmep__assistant=assistant).exclude(id=mep.id)
