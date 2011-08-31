# Create your views here.

from models import Campaign
from django.shortcuts import render_to_response, get_object_or_404
from campaign.forms import ScoreForm
from campaign.models import MEPScore
from django.template import RequestContext
from meps.models import MEP, OrganizationMEP
from datetime import date

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
        #query=OrganizationMEP.objects.filter(organization__name__in=form.cleaned_data['staff'])
        #print query.count()
        #print '\n'.join([str((x.end,x.mep,x.organization)) for x in query]).decode('utf8')
        #query=query.filter(end=date(9999, 12, 31))
        #print query.count()
        #print '\n'.join([str((x.end,x.mep,x.organization)) for x in query]).decode('utf8')
        query['organizationmep__organization__name__in']=form.cleaned_data['staff']
        query['organizationmep__end']=date(9999, 12, 31)
        if form.cleaned_data['staffRole']:
            #query=query.filter(role__in=form.cleaned_data['staffRole'])
            query['organizationmep__role__in']=form.cleaned_data['staffRole']
            query['organizationmep__end']=date(9999, 12, 31)
        #meps.extend([x.mep for x in query])

    if form.cleaned_data['committee']:
        query['committeerole__committee__name__in']=form.cleaned_data['committee']
        query['committeerole__end']=date(9999, 12, 31)
        if form.cleaned_data['committeeRole']:
            query['committeerole__role__in']=form.cleaned_data['committeeRole']
            query['committeerole__end']=date(9999, 12, 31)

    #print meps
    #if meps:
    if query:
        for mep in MEP.objects.filter(**query).distinct():
        #for mep in meps:
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
