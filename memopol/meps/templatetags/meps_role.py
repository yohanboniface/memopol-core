from django import template

from memopol.meps.models import OrganizationMEP, CommitteeRole, DelegationRole

register = template.Library()


@register.simple_tag
def current_organization_role(mep, organization):
    roles = OrganizationMEP.objects.filter(mep=mep, organization=organization)
    roles = sorted([role.role for role in roles if role.role != 'Member'])
    return roles and roles[0] or ''


@register.simple_tag
def current_committee_role(mep, committee):
    roles = CommitteeRole.objects.filter(mep=mep, committee=committee)
    roles = sorted([role.role for role in roles if role.role != 'Member'])
    return roles and roles[0] or ''


@register.simple_tag
def current_delegation_role(mep, delegation):
    roles = DelegationRole.objects.filter(mep=mep, delegation=delegation)
    roles = sorted([role.role for role in roles if role.role != 'Member'])
    return roles and roles[0] or ''
