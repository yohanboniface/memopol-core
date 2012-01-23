from meps.models import OrganizationMEP, CommitteeRole, DelegationRole
from django import template

register = template.Library()

@register.simple_tag
def current_organization_role(mep, organization):
    return OrganizationMEP.objects.get(mep=mep, organization=organization).role

@register.simple_tag
def current_committee_role(mep, committee):
    return CommitteeRole.objects.get(mep=mep, committee=committee).role

@register.simple_tag
def current_delegation_role(mep, delegation):
    return DelegationRole.objects.get(mep=mep, delegation=delegation).role
