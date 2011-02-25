# Create your views here.

from django.shortcuts import render_to_response
from forms import QueryForm
from models import MEP

def query(request):
    form = QueryForm(request.GET)
    if not form.is_valid():
        return render_to_response('query.html')
    print form.cleaned_data
    #meps = MEP.view('meps/query', { 'key': form.cleaned_data.get('commitee_filter')})
    #return render_to_response('query.html', { 'meps': meps})
    return render_to_response('query.html')
