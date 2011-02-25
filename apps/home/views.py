from home.models import Edito
from meps.models import MEP
from votes.models import Vote
from django.views.generic.simple import direct_to_template

def home(request):
    #Les 7 lignes a venir sont un peu degueu
    homes = Edito.objects.all()
    if homes:
        edito_title = homes[0].edito_title
        edito = homes[0].edito
    else:
        edito_title = ''
        edito = ''

    groups = list(MEP.view('meps/groups', group=True))
    groups.sort(key=lambda group: group['value']['count'], reverse=True)

    countries = list(MEP.view('meps/countries', group=True))
    countries.sort(key=lambda group: group['value']['count'], reverse=True)

    votes = Vote.view('votes/all')

    context = {
        'groups': groups,
        'countries': countries,
        'votes': votes,
        'edito_title': edito_title,
        'edito' : edito
    }
    return direct_to_template(request, 'home.html', context)


