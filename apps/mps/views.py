from urllib import urlopen
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify

from models import MP

def get_nosdeputes_widget(request, pk):
    mp = get_object_or_404(MP, id=pk)
    return HttpResponse(urlopen("http://www.nosdeputes.fr/widget/%s-%s" % (slugify(mp.first_name), slugify(mp.last_name))).read().replace("935", "800"))
