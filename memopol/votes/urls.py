from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect

from memopol.votes.models import Proposal, RecommendationData

from memopol.votes.feeds import LatestProposalsFeed


def dont_broke_old_urls(request, pk):
    get_object_or_404(Proposal, pk=pk)
    return redirect(request.path.replace("/votes", "/europe/parliament/vote"))


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Proposal), name='index'),
    url(r'^import/$', ListView.as_view(model=RecommendationData, paginate_by=100), name='import'),
    url(r'^import/(?P<pk>\d+)/$', DetailView.as_view(model=RecommendationData), name='import_vote'),
    url(r'^latest/feed', LatestProposalsFeed(), name='lastest-rss'),
    url(r'^(?P<pk>[a-zA-Z/-_]+)/(.*)$', dont_broke_old_urls),
)
