# Create your views here.

from forms import QueryForm
from django.shortcuts import render_to_response

def query(request):
    form = UploadForm(request.POST)
    return render_to_response('view.html', { 'doc': data})
