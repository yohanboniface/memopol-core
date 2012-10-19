# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from . import views


urlpatterns = patterns('',  # pylint: disable=C0103
    url(r'^xhr/$', views.XhrSearchView.as_view(), name='search_xhr'),
    url(r'^$', views.SearchView.as_view(), name='search'),
)
