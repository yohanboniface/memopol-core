from django.views.generic.simple import direct_to_template

from votes.models import Vote

def index(request):
    votes = Vote.view('main/all')
    context = {
        'votes': votes,
    }
    return direct_to_template(request, 'votes/index.html', context)

def detail(request, vote_name):
    votes = Vote.view('main/by_name', key=vote_name)
    context = {
        'vote': votes.first(),
    }
    return direct_to_template(request, 'votes/detail.html', context)

