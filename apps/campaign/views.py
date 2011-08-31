# Create your views here.

from models import Campaign
from django.shortcuts import render_to_response, get_object_or_404
from campaign.forms import ScoreForm
from django.template import RequestContext

def updateCampaignScores(form, pk):
    #{'group': [u'alde'], 'committee': [], 'delegation': [], 'score': -10, 'committeeRole': [], 'groupRole': [u'chair', u'chairofthebureau', u'co-chair', u'deputychair', u'deputytreasurer', u'member', u'treasurer', u'vice-chair', u'vice-chair/memberofthebureau'], 'staffRole': [], 'delegationRole': [], 'staff': []}
    if 'groupRole' in form.cleaned_data:
        print form.cleaned_data['groupRole']

def editCampaign(request, pk):
    c=get_object_or_404(Campaign, pk=pk)
    data={ 'campaign': c }
    form = ScoreForm(request.POST)
    if not form.is_valid():
        form = ScoreForm()
    else:
        updateCampaignScores(form, pk)
    data['form']=form
    return render_to_response('campaign/edit.html',
                              data,
                              context_instance = RequestContext(request))
