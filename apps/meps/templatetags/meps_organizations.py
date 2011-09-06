from datetime import date
from meps.models import OrganizationMEP
from django import template

register = template.Library()

@register.simple_tag
def current_organization_role(mep, organization):
    return OrganizationMEP.objects.get(mep=mep, organization=organization, end=date(9999, 12, 31)).role
