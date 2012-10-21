# Create your views here.
from django.conf import settings
from django.shortcuts import render
import re, json, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404

from models import Dossier, Committee, Amendment
from utils import fetch, committee_map

dossiermask=re.compile(r'[0-9]{4}/[0-9]{4}\([A-Z]{3}\)')

def fetchams(ref):
    try:
        dj = json.load(fetch("%s/dossier/%s?format=json" % (settings.PARLTRACK_URL,ref)))
    except:
        raise ValueError
    dossier,_ = Dossier.objects.get_or_create(id=ref,
                                              title=dj['procedure']['title'],
                                              _date=datetime.datetime.now())
    committees={}
    for am in dj['amendments']:
        for committee in am['committee']:
            date=am['date'].split('T')[0]
            id=committee_map.get(committee,committee)
            if not (id,date) in committees:
                c,_=Committee.objects.get_or_create(dossier=dossier,
                                                          title=committee,
                                                          cid=id,
                                                          src = am['src'],
                                                          date=date)
                committees[(id, date)]=c
            else:
                c=committees[(id,date)]
            a,_=Amendment.objects.get_or_create(seq = am['seq'],
                                                dossier = dossier,
                                                committee = c,
                                                lang = am['orig_lang'],
                                                authors = am['authors'],
                                                new = '\n'.join(am.get('new',[])),
                                                old = '\n'.join(am.get('old',[])),
                                                type = am['location'][0][0],
                                                location = am['location'][0][1])
    return dossier

def dossiers(request):
    queryset = Dossier.objects.all()
    return render(request, "pom_list_dossiers.html", {"dossiers": queryset })

def dossier(request):
    ref=request.GET.get('id').upper()
    if not dossiermask.match(ref):
        raise ValueError # TODO
    try:
        dossier = Dossier.objects.get(id=ref)
    except ObjectDoesNotExist:
        dossier = fetchams(ref)
    # already cached
    queryset = Committee.objects.filter(dossier=dossier)
    return render(request, "pom_list_committees.html", {"dossier": dossier, 'committees': queryset})

def amendments(request,cid):
    c = Committee.objects.get(pk=cid)
    ams = Amendment.objects.filter(committee=c)
    return render(request, "pom_list_amendments.html", {"ams": ams, "committee": c})

def score(request):
    amid=int(request.POST.get('amid'))
    print amid
    print request.user
    print request.POST.get('value')
    return HttpResponse('ok')

def comment(request):
    amid=int(request.POST.get('amid'))
    print amid
    print request.user
    print request.POST.get('comment')
    return HttpResponse('ok')
