# Create your views here.

from models import Campaign
from django.shortcuts import render_to_response, get_object_or_404
from campaign.forms import ScoreForm
from campaign.models import MEPScore, ScoreRule
from django.template import RequestContext
from django.http import HttpResponse #, HttpResponseRedirect, Http404
from meps.models import MEP, OrganizationMEP
from datetime import date
import random, json

def updateCampaignScores(form, pk, c):
    #meps=[]
    query={}
    if form.cleaned_data['group']:
        query['groupmep__group__abbreviation__in']=form.cleaned_data['group']
        query['groupmep__end']=date(9999, 12, 31)
        if form.cleaned_data['groupRole']:
            query['groupmep__role__in']=form.cleaned_data['groupRole']
            query['groupmep__end']=date(9999, 12, 31)

    if form.cleaned_data['delegation']:
        query['delegationrole__delegation__name__in']=form.cleaned_data['delegation']
        query['delegationrole__end']=date(9999, 12, 31)
        if form.cleaned_data['delegationRole']:
            query['delegationrole__role__in']=form.cleaned_data['delegationRole']
            query['delegationrole__end']=date(9999, 12, 31)

    if form.cleaned_data['staff']:
        query['organizationmep__organization__name__in']=form.cleaned_data['staff']
        query['organizationmep__end']=date(9999, 12, 31)
        if form.cleaned_data['staffRole']:
            query['organizationmep__role__in']=form.cleaned_data['staffRole']
            query['organizationmep__end']=date(9999, 12, 31)
        #meps.extend([x.mep for x in query])

    if form.cleaned_data['committee']:
        query['committeerole__committee__name__in']=form.cleaned_data['committee']
        query['committeerole__end']=date(9999, 12, 31)
        if form.cleaned_data['committeeRole']:
            query['committeerole__role__in']=form.cleaned_data['committeeRole']
            query['committeerole__end']=date(9999, 12, 31)

    print ', '.join(["%s = %s" % (k,v) for k,v in query.items()])
    if query:
        # for the record
        ScoreRule(campaign=c,
                  rule=', '.join(["%s = %s" % (k,v) for k,v in query.items()]),
                  score=form.cleaned_data['weight']).save()
        for mep in MEP.objects.filter(**query).distinct():
            ms=MEPScore.objects.get_or_create(mep=mep, campaign=c)[0]
            ms.score+=form.cleaned_data['weight']
            ms.save()

def editCampaign(request, pk):
    c=get_object_or_404(Campaign, pk=pk)
    data={ 'campaign': c }
    form = ScoreForm(request.POST)
    if not form.is_valid():
        form = ScoreForm()
    else:
        updateCampaignScores(form, pk, c)
    data['form']=form
    return render_to_response('campaign/edit.html',
                              data,
                              context_instance = RequestContext(request))

def randomsubset(l, n):
    res=[]
    for _ in xrange(n):
        res.append(random.choice([x for li in [[x[1]] * x[0] for x in l if x[1] not in res] for x in li]))
    return res

def getCampaignMeps(request, pk):
    c=get_object_or_404(Campaign, pk=pk)
    scoredmeps=[(x['score'],x['mep']) for x in MEPScore.objects.filter(campaign=c).values('mep','score')]
    smeps=set([x[1] for x in scoredmeps])
    allmeps=set([x['id'] for x in MEP.objects.filter(active=True).values('id')])
    zmeps=[(1, x) for x in allmeps-smeps]
    chosen=randomsubset(zmeps+scoredmeps, request.GET.get('limit',10))
    if request.GET.get('format')=='json':
        return HttpResponse(json.dumps(chosen),
                            mimetype="application/json")
    return render_to_response('campaign/list.html',
                              { 'object_list': [MEP.objects.get(pk=x) for x in chosen] },
                              context_instance = RequestContext(request))
