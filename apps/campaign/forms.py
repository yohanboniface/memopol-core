from django import forms
from datetime import datetime
from django.conf import settings
from django.utils.translation import ugettext as _
from meps.models import GroupMEP, CommitteeRole, DelegationRole, OrganizationMEP, MEP, Committee, Group, Organization, Delegation

class ScoreForm(forms.Form):
   weight = forms.IntegerField(required=True)
   committee = forms.MultipleChoiceField(required=False,
                                         choices=(('',''),)+tuple([(x['name'], x['name'])
                                                                   for x in Committee.objects.filter(committeerole__mep__active=True).values('name').distinct()]))
   committeeRole = forms.MultipleChoiceField(required=False,
                                             choices=(('',''),)+tuple([(x['role'], x['role'])
                                                                       for x in CommitteeRole.objects.filter(mep__active=True).values('role').distinct()]))
   group = forms.MultipleChoiceField(required=False,
                                     choices=(('',''),)+tuple([(x['abbreviation'], x['abbreviation'])
                                                               for x in Group.objects.filter(groupmep__mep__active=True).values('abbreviation').distinct()]))
   groupRole = forms.MultipleChoiceField(required=False,
                                         choices=(('',''),)+tuple([(x['role'], x['role'])
                                                                   for x in GroupMEP.objects.filter(mep__active=True).values('role').distinct()]))
   staff = forms.MultipleChoiceField(required=False,
                                     choices=(('',''),)+tuple([(x['name'], x['name'])
                                                               for x in Organization.objects.filter(organizationmep__mep__active=True).values('name').distinct()]))
   staffRole = forms.MultipleChoiceField(required=False,
                                         choices=(('',''),)+tuple([(x['role'], x['role'])
                                                                   for x in OrganizationMEP.objects.filter(mep__active=True).values('role').distinct()]))
   delegation = forms.MultipleChoiceField(required=False,
                                          choices=(('',''),)+tuple([(x['name'], x['name'])
                                                                    for x in Delegation.objects.filter(delegationrole__mep__active=True).values('name').distinct()]))
   delegationRole = forms.MultipleChoiceField(required=False,
                                              choices=(('',''),)+tuple([(x['role'], x['role'])
                                                                        for x in DelegationRole.objects.filter(mep__active=True).values('role').distinct()]))
