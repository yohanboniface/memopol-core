from django import forms
from datetime import datetime
from django.conf import settings
from django.utils.translation import ugettext as _
from meps.models import GroupMEP, CommitteeRole, DelegationRole, OrganizationMEP, MEP, Committee, Group, Organization, Delegation

class ScoreForm(forms.Form):
   score = forms.IntegerField(required=True)
   groupRole = forms.MultipleChoiceField(required=False,
                                 choices=(('',''),)+tuple([(''.join(x['role'].lower().split()), x['role'])
                                                           for x in GroupMEP.objects.filter(mep__active=True).values('role').distinct()]))
   group = forms.MultipleChoiceField(required=False,
                                     choices=(('',''),)+tuple([(''.join(x['abbreviation'].lower().split()), x['abbreviation'])
                                                               for x in Group.objects.filter(groupmep__mep__active=True).values('abbreviation').distinct()]))
   staffRole = forms.MultipleChoiceField(required=False,
                                 choices=(('',''),)+tuple([(''.join(x['role'].lower().split()), x['role'])
                                                           for x in OrganizationMEP.objects.filter(mep__active=True).values('role').distinct()]))
   staff = forms.MultipleChoiceField(required=False,
                                     choices=(('',''),)+tuple([(''.join(x['name'].lower().split()), x['name'])
                                                               for x in Organization.objects.filter(organizationmep__mep__active=True).values('name').distinct()]))
   committeeRole = forms.MultipleChoiceField(required=False,
                                     choices=(('',''),)+tuple([(''.join(x['role'].lower().split()), x['role'])
                                                               for x in CommitteeRole.objects.filter(mep__active=True).values('role').distinct()]))
   committee = forms.MultipleChoiceField(required=False,
                                         choices=(('',''),)+tuple([(''.join(x['name'].lower().split()), x['name'])
                                                                   for x in Committee.objects.filter(committeerole__mep__active=True).values('name').distinct()]))
   delegationRole = forms.MultipleChoiceField(required=False,
                                      choices=(('',''),)+tuple([(''.join(x['role'].lower().split()), x['role'])
                                                                for x in DelegationRole.objects.filter(mep__active=True).values('role').distinct()]))
   delegation = forms.MultipleChoiceField(required=False,
                                          choices=(('',''),)+tuple([(''.join(x['name'].lower().split()), x['name'])
                                                                    for x in Delegation.objects.filter(delegationrole__mep__active=True).values('name').distinct()]))
