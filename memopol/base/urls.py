from django.contrib.sitemaps import GenericSitemap
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from memopol.mps.models import MP

from memopol.base.api import v1_api
from memopol.base import views

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

#home_mimetype = 'application/xhtml+xml'  # required for embedded SVG
if settings.APPS_DEBUG:
    home_mimetype = 'text/html'  # compliant with django-debug-toolbar (debug mode)


class RobotsTxt(TemplateView):
    template_name = "robots.txt"

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['mimetype'] = 'text/plain'
        return super(TemplateView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(RobotsTxt, self).get_context_data(**kwargs)
        context["DEBUG"] = settings.DEBUG
        return context

urlpatterns = patterns('',  # pylint: disable=C0103
    url(r'^$', views.home, name='index'),
    url(r'^api/$', direct_to_template, {'template': 'api.html', 'extra_context': {"root_url": settings.ROOT_URL}}, name='api_doc'),
    url(r'^europe/parliament/', include('memopol.meps.urls', namespace='meps', app_name='meps')),
    url(r'^france/assemblee/', include('memopol.mps.urls', namespace='mps', app_name='mps')),
    url(r'^votes/', include('memopol.votes.urls', namespace='votes', app_name='votes')),
    url(r'^patches/', include('memopol.patch_o_maton.urls', namespace='patch_o_maton', app_name='patch_o_maton')),
    url(r'^trends/', include('memopol.trends.urls', namespace='trends', app_name='trends')),
    url(r'^campaign/', include('memopol.campaign.urls', namespace='campaign', app_name='campaign')),
    url(r'^search/', include('memopol.search.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^contact/', include('contact_form.urls')),
    url(r'^robots\.txt$', RobotsTxt.as_view()),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^ajax_select/', include('ajax_select.urls')),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
