from django.template import Library
from django.conf import settings


register = Library()


@register.assignment_tag
def organization_name():
    return settings.ORGANIZATION_NAME
