from meps.models import *
from django.views.genric.simple import direct_to_template

def addTrophy(request):

    return direct_to_template(request, 'trophy.html', context)
