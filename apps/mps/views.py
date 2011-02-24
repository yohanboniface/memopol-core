from django.views.generic.simple import direct_to_template

from mps.models import MP

def index(request):
    mps = MP.view('mps/all')
    context = {
        'mps': mps,
    }
    return direct_to_template(request, 'mps/index.html', context)

def detail(request, mp_id):
    mps = MP.view('mps/by_id', key=mp_id)
    context = {
        'mp': mps.first(),
    }
    return direct_to_template(request, 'mps/detail.html', context)

