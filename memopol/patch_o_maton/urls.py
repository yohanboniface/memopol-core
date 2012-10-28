from django.conf.urls.defaults import patterns, url, include
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

#from meps.models import LocalParty, Country, Group, Committee, Delegation, Organization, Building, MEP
#from reps.models import Opinion

from views import dossiers, dossier, amendments, score, comment #BuildingDetailView, MEPView, MEPsFromView, MEPList, PartyView

urlpatterns = patterns('memopol.patch_o_maton.views',
                       url(r'^dossiers/$', dossiers ),
                       url(r'^dossier/$', dossier ),
                       url(r'^amendments/(?P<cid>[0-9]*)/$', amendments ),
                       url(r'^score/$', score ),
                       url(r'^comment/$', comment ),
                       )
