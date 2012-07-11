# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from search import views

urlpatterns = patterns('', # pylint: disable=C0103
    url(r'^xhr/$', views.search, {'template_name': 'search_xhr.html'}, name='search_xhr'),
    url(r'^$', views.search, {'template_name': 'search.html'}, name='search'),
)
