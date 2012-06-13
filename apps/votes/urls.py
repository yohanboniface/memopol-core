from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView

from votes.models import Proposal, RecommendationData

from votes.feeds import LatestProposalsFeed

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Proposal), name='index'),
    url(r'^import/$', ListView.as_view(model=RecommendationData), name='import'),
    url(r'^import/(?P<pk>\d+)/$', DetailView.as_view(model=RecommendationData), name='import_vote'),
    url(r'^latest/feed', LatestProposalsFeed(), name='lastest-rss'),
)
