# Create your views here.

from django.shortcuts import render_to_response
from forms import QueryForm

from django.views.generic.simple import direct_to_template

from meps.models import MEP

def query(request):
    form = QueryForm(request.GET)
    if not form.is_valid():
        return render_to_response('query.html')
    key=[]
    #for fltr in ('commitee_filter', 'group_filter', 'country_filter'):
    #    val=form.cleaned_data.get(fltr)
    #    if val: key.append(val)
    key=[u'DE', u'PPE', form.cleaned_data.get('commitee_filter',None)]
         #form.cleaned_data.get('political_filter',None),
         #form.cleaned_data.get('country_filter',None))
    print key
    meps = MEP.view('meps/query', key=key)
    print list(meps)
    return render_to_response('query.html', { 'meps': meps})

def bla(request):
    meps_by_name = MEP.view('meps/by_name')
    countries = list(MEP.view('meps/countries', group=True))
    context = {
        'meps': meps_by_name,
        'countries': countries,
    }
    return direct_to_template(request, 'query.html', context)
