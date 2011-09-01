from django.conf.urls.defaults import patterns, url
from campaign import views as CampaignView
from meps.models import Country, Group, Committee, Delegation, Organization, Building

urlpatterns = patterns('campaign.views',
    url(r'^edit/(?P<pk>\w+)/$', CampaignView.editCampaign, ),
    url(r'^view/(?P<pk>\w+)/$', CampaignView.getCampaignMeps, ),
)
