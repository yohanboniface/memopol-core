# Create your views here.

from models import Campaign, Debriefing
from campaign.forms import ScoreForm, DebriefingForm
from campaign.models import MEPScore, ScoreRule
from meps.models import MEP

from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect #, Http404
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from datetime import date
from itertools import izip
from email.mime.text import MIMEText
import random, json, hashlib, smtplib

def updateCampaignScores(form, pk, c):
    query={}

    if form.cleaned_data['group']:
        query['groupmep__group__abbreviation__in'] = form.cleaned_data['group']
        query['groupmep__end'] = date(9999, 12, 31)

        if form.cleaned_data['groupRole']:
            query['groupmep__role__in'] = form.cleaned_data['groupRole']

    if form.cleaned_data['delegation']:
        query['delegationrole__delegation__name__in'] = form.cleaned_data['delegation']
        query['delegationrole__end'] = date(9999, 12, 31)

        if form.cleaned_data['delegationRole']:
            query['delegationrole__role__in'] = form.cleaned_data['delegationRole']

    if form.cleaned_data['staff']:
        query['organizationmep__organization__name__in'] = form.cleaned_data['staff']
        query['organizationmep__end'] = date(9999, 12, 31)

        if form.cleaned_data['staffRole']:
            query['organizationmep__role__in'] = form.cleaned_data['staffRole']

    if form.cleaned_data['committee']:
        query['committeerole__committee__name__in'] = form.cleaned_data['committee']
        query['committeerole__end'] = date(9999, 12, 31)

        if form.cleaned_data['committeeRole']:
            query['committeerole__role__in'] = form.cleaned_data['committeeRole']

    #print ', '.join(["%s = %s" % (k,v) for k,v in query.items()])
    if query:
        # for the record
        ScoreRule(campaign=c,
                  rule=', '.join(["%s = %s" % (k,v) for k,v in query.items()]),
                  score=form.cleaned_data['weight']).save()

        for mep in MEP.objects.filter(**query).distinct():
            ms = MEPScore.objects.get_or_create(mep=mep, campaign=c)[0]
            ms.score += form.cleaned_data['weight']
            ms.save()

def editCampaign(request, pk):
    c = get_object_or_404(Campaign, pk=pk)
    if not request.user.is_authenticated():
        messages.add_message(request,
                             messages.ERROR,
                             "You should login to edit the campaign.")
        return HttpResponseRedirect("/campaign/view/%s/" % c.id)
    data = { 'campaign': c }
    form = ScoreForm(request.POST)
    if not form.is_valid():
        form = ScoreForm()
    else:
        updateCampaignScores(form, pk, c)
    data['form'] = form
    return render_to_response('campaign/edit.html',
                              data,
                              context_instance = RequestContext(request))

def randomsubset(l, n):
    res = []
    for _ in xrange(n):
        res.append(random.choice([x for li in [[x[1]] * x[0] for x in l if x[1] not in res] for x in li]))
    return res

def getCampaignMeps(request, pk):
    c=get_object_or_404(Campaign, pk=pk)
    if not 'chosen' in request.session:
        request.session['chosen']={}
    if not c in request.session['chosen'] or request.GET.get('force'):
        scoredmeps=[(x['score'],x['mep']) for x in MEPScore.objects.filter(campaign=c).values('mep','score')]
        smeps=set([x[1] for x in scoredmeps])
        allmeps=set([x['id'] for x in MEP.objects.filter(active=True).values('id')])
        zmeps=[(1, x) for x in allmeps-smeps]
        try:
            limit=int(request.GET.get('limit'))
        except:
            limit=3
        chosen=randomsubset(zmeps+scoredmeps, limit)
        request.session['chosen'][c]=chosen
        request.session.modified = True
        return HttpResponseRedirect("/campaign/view/%s/" % c.id)
    else:
        chosen=request.session['chosen'][c]
    if request.GET.get('format')=='json':
        return HttpResponse(json.dumps(chosen),
                            mimetype="application/json")

    chosen=[MEP.objects.get(pk=x) for x in chosen]
    forms = [DebriefingForm(instance=Debriefing(mep=mep,campaign=c)) for mep in chosen]
    dbriefs = [Debriefing.objects.filter(mep=mep,campaign=c,valid="") for mep in chosen]
    return render_to_response('campaign/view.html',
                              { 'object_list': izip(chosen,forms, dbriefs ),
                                'campaign': c, },
                              context_instance = RequestContext(request))

def getCampaigns(request):
    c=[(c, MEP.objects.filter(debriefing__campaign=c).distinct().count()) for c in Campaign.objects.all()]
    return render_to_response('campaign/list.html',
                              { 'object_list': c, },
                              context_instance = RequestContext(request))

def feedback(request):
    feedback = DebriefingForm(request.POST)
    feedback.full_clean()
    if feedback.errors:
        return HttpResponse(str(feedback.errors))
    feedback = feedback.save(commit=False)
    tmp=Debriefing.objects.filter(mep=feedback.mep,
                                  campaign=feedback.campaign,
                                  usercontact=feedback.usercontact,
                                  type=feedback.type,
                                  response=feedback.response,
                                  text=feedback.text).count()
    if tmp>0:
        return HttpResponse("known.")
    feedback.save()
    to=[x.email for x in User.objects.filter(is_staff=True)]
    actid=sendverifymail(feedback,to)
    feedback.valid=actid
    feedback.save()
    return HttpResponse("Thank you.")

def sendverifymail(feedback,to):
    actid = hashlib.sha1(''.join([chr(random.randint(32, 122))
                                  for x in range(12)])).hexdigest()
    msg = MIMEText(_("Someone sent feedback on a campaign\nYour verification key is %(root_url)s/campaign/feedback/%(feedback_id)s/%(actid)s\n\nfrom: %(from)s\nabout %(mep)s\ntype: %(type)s\nresult: %(result)s\ncomment: %(comment)s")
                   % {"root_url": settings.ROOT_URL or 'http://localhost:8001/',
                      "feedback_id": feedback.id,
                      "actid": actid,
                      "from": feedback.usercontact,
                      "mep": feedback.mep,
                      "type": feedback.type,
                      "result": feedback.response,
                      "comment": feedback.text})
    msg['Subject'] = _('Memopol2 feedback moderation')
    msg['From'] = 'memopol2@memopol2.lqdn.fr'
    msg['To'] = ', '.join(to)
    s = smtplib.SMTP('localhost')
    s.sendmail('memopol2@memopol2.lqdn.fr', [to], msg.as_string())
    s.quit()
    return actid

def confirm(request, id, key):
    feedback=None
    try:
        feedback=Debriefing.objects.get(pk=id, valid=key)
    except ObjectDoesNotExist:
        messages.add_message(request,
                             messages.INFO,
                             "Thank you! Either already confirmed, or object doesn't exist")
        return HttpResponseRedirect('/campaign/list/')
    feedback.valid=''
    feedback.save()
    messages.add_message(request,
                         messages.INFO,
                         'Thank you for your confirmation')
    return HttpResponseRedirect('/campaign/view/%s/' % feedback.campaign.id)

def report(request, pk):
    c=get_object_or_404(Campaign, pk=pk)
    chosen=MEP.objects.filter(debriefing__campaign=c,debriefing__valid="").distinct()
    forms = [DebriefingForm(instance=Debriefing(mep=mep,campaign=c,valid="")) for mep in chosen]
    dbriefs = [Debriefing.objects.filter(mep=mep,campaign=c,valid="") for mep in chosen]
    mepscores = MEPScore.objects.filter(campaign=c)
    mepsforms = [DebriefingForm(instance=Debriefing(mep=mep,campaign=c,valid=""))
                 for mep in MEP.objects.filter(mepscore__campaign=c)]
    return render_to_response('campaign/view.html',
                              { 'object_list': izip(chosen,forms, dbriefs ),
                                'mepscores': izip(mepscores,mepsforms),
                                'campaign': c, },
                              context_instance = RequestContext(request))
