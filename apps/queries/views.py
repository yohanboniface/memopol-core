# Create your views here.

from forms import QueryForm
from django.shortcuts import render_to_response
from model import MEP

def query(request):
    form = QueryForm(request.POST)
    meps = MEP.view('meps/query', { 'key': form.cleaned_data.get('commitee_filter'))
    return render_to_response('query.html', { 'meps': meps})
