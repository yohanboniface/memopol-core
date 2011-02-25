from django import forms
from datetime import datetime
from django.conf import settings
from django.utils.translation import ugettext as _

class QueryForm(forms.Form):
   country =forms.CharField(required=False, label=_("Constituent Country"))
   party = forms.CharField(widget=AdvancedEditor(), label=_("Political Group"))
   commitee = forms.CharField(required=False, label=_("Commitee"))
