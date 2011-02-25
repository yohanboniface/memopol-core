# Create your views here.

from django.shortcuts import render_to_response
from forms import QueryForm

from django.views.generic.simple import direct_to_template

from meps.models import MEP

def query(request):
    form = QueryForm(request.GET)
    if not form.is_valid():
        return render_to_response('query.html')
    meps = MEP.view('meps/query', key=form.cleaned_data.get('commitee_filter'))
    return render_to_response('query.html', { 'meps': meps})

def bla(request):
    meps_by_name = MEP.view('meps/by_name')
    context = {
        'meps': meps_by_name,
    }
    return direct_to_template(request, 'query.html', context)
