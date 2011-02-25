# Create your views here.

from forms import QueryForm
from django.shortcuts import render_to_response
from model import MEP

def query(request):
    form = UploadForm(request.POST)
    meps = MEP.view('meps/query')
    return render_to_response('view.html', { 'meps': meps})
