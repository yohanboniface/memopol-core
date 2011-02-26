from django.forms import *
from meps.models import *

class TrophyForm(ModelForm):
    class Meta:
        model = Trophy

class AutoTrophyForm(TrophyForm):
    class Meta:
        model = AutoTrophy

class ManualTrophyForm(TrophyForm):
    class Meta:
        model = ManualTrophy
