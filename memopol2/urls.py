import os

from django.contrib.sitemaps import GenericSitemap
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from mps.models import MP
from meps.models import Committee
from votes.models import Proposal

from memopol2.api import v1_api

admin.autodiscover()

sitemeps_dict = {
    'queryset': MP.objects.all(),
    #'date_field': 'pub_date',
}

sitemps_dict = {
    'queryset': MP.objects.all(),
    #'date_field': 'pub_date',
}

sitemaps = {
    'meps': GenericSitemap(sitemeps_dict, priority=0.6),
    'mps': GenericSitemap(sitemps_dict, priority=0.6),
}

home = {
    'committees': Committee.objects.order_by('abbreviation').all(),
    'proposals': Proposal.objects.all()
}

#home_mimetype = 'application/xhtml+xml'  # required for embedded SVG
if settings.APPS_DEBUG:
    home_mimetype = 'text/html'  # compliant with django-debug-toolbar (debug mode)


class RobotsTxt(TemplateView):
    template_name="robots.txt"

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['mimetype'] = 'text/plain'
        return super(TemplateView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(RobotsTxt, self).get_context_data(**kwargs)
        context["DEBUG"] = settings.DEBUG
        return context


urlpatterns = patterns('', # pylint: disable=C0103
    url(r'^$', direct_to_template, {'template': 'home.html', 'extra_context': home}, name='index'),
    url(r'^api/$', direct_to_template, {'template': 'api.html', 'extra_context': {"root_url": settings.ROOT_URL}}, name='api_doc'),
    url(r'^europe/parliament/', include('meps.urls', namespace='meps', app_name='meps')),
    url(r'^france/assemblee/', include('mps.urls', namespace='mps', app_name='mps')),
    url(r'^votes/', include('votes.urls', namespace='votes', app_name='votes')),
    url(r'^trends/', include('trends.urls', namespace='trends', app_name='trends')),
    url(r'^campaign/', include('campaign.urls', namespace='campaign', app_name='campaign')),
    url(r'^search/', include('search.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^contact/', include('contact_form.urls')),
    url(r'^robots\.txt$', RobotsTxt.as_view()),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^api/', include(v1_api.urls)),
)

# hack to autodiscover static files location in dev mode
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(.*)$', serve, {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
    )
# TODO: static files location in production
# should never be served by django, settings.MEDIA_URL is the right way to do
