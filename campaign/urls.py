from django.conf.urls.defaults import patterns, url
from campaign import views as CampaignView

urlpatterns = patterns('campaign.views',
    url(r'^list/$', CampaignView.getCampaigns, name="list"),
    url(r'^edit/(?P<pk>[0-9]+)/$', CampaignView.editCampaign, name="edit"),
    url(r'^view/(?P<pk>[0-9]+)/$', CampaignView.getCampaignMeps, name="view"),
    url(r'^report/(?P<pk>[0-9]+)/$', CampaignView.report, name="report"),
    url(r'^feedback/$', CampaignView.feedback, name="feedback"),
    url(r'^feedback/(?P<id>[0-9]+)/(?P<key>[0-9a-f]+)/$', CampaignView.confirm, name="confirm" ),
)
