from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail
from memopol2 import utils

from mps.models import MP, Group, Department

urlpatterns = patterns('',
    # the /names view is *very* expansive. we cache it in RAM for a week
    url(r'^$', utils.cached(3600*24*7)(list_detail.object_list), {'queryset': MP.objects.filter(active=True)}, name='index'),

    url(r'^depute/(?P<object_id>[a-zA-Z]+)/$', list_detail.object_detail, {'queryset': MP.objects.all(), 'template_object_name': 'mp'}, name='mp'),
    url(r'^depute/(?P<object_id>[a-zA-Z]+)/contact$', list_detail.object_detail, {'queryset': MP.objects.all(), 'template_object_name': 'mp', 'template_name': 'mp/mp_contact.html'}, name='mp_contact'),
    url(r'^group/$', list_detail.object_list, {'queryset': Group.objects.all()}, name='index_groups'),
    url(r'^group/(?P<object_id>.+)/$', list_detail.object_detail, {'queryset': Group.objects.all(), 'template_name': 'mps/container_detail.html'}, name='index_by_group'),
    url(r'^department/$', list_detail.object_list, {'queryset': Department.objects.all().order_by('number')}, name='index_departments'),
    url(r'^department/(?P<object_id>.+)/$', list_detail.object_detail, {'queryset': Department.objects.all(), 'template_name': 'mps/container_detail.html'}, name='index_by_department'),
)
