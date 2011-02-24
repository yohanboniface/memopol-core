from django.views.generic.simple import direct_to_template

from votes.models import Vote

def index_votes(request):
    votes = Vote.view('main/all')
    context = {
        'votes': votes,
    }
    return direct_to_template(request, 'votes/votes.html', context)

def vote(request, vote_name):
    votes = Vote.view('main/by_name', key=vote_name)
    context = {
        'vote': votes.first(),
    }
    return direct_to_template(request, 'votes/vote.html', context)

