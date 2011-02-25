from django import forms
from datetime import datetime
from django.conf import settings
from django.utils.translation import ugettext as _

class QueryForm(forms.Form):
   country_filter =forms.CharField(required=False, label=_("Constituent Country"))
   party_filter = forms.CharField(required=False, label=_("Political Group"))
   commitee_filter = forms.CharField(required=False, label=_("Commitee"))
