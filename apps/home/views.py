from votes.models import Vote
from django.views.generic.simple import direct_to_template

def home(request):


    votes = Vote.view('votes/all', descending=True)

    context = {
        'votes': votes,
    }
    return direct_to_template(request, 'home.html', context)


