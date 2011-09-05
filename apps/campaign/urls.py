from django.conf.urls.defaults import patterns, url
from campaign import views as CampaignView
from meps.models import Country, Group, Committee, Delegation, Organization, Building

urlpatterns = patterns('campaign.views',
    url(r'^list/$', CampaignView.getCampaigns, ),
    url(r'^edit/(?P<pk>[0-9]+)/$', CampaignView.editCampaign, ),
    url(r'^view/(?P<pk>[0-9]+)/$', CampaignView.getCampaignMeps, ),
    url(r'^report/(?P<pk>[0-9]+)/$', CampaignView.report, ),
    url(r'^feedback/$', CampaignView.feedback, ),
    url(r'^feedback/(?P<id>[0-9]+)/(?P<key>[0-9a-f]+)/$', CampaignView.confirm, ),
)
