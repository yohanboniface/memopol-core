from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail

from mps.models import MP, Group, Department

urlpatterns = patterns('',
    url(r'^$', list_detail.object_list, {'queryset': MP.objects.filter(active=True)}, name='index'),
    url(r'^depute/(?P<object_id>[a-zA-Z]+)/$', list_detail.object_detail, {'queryset': MP.objects.all(), 'template_object_name': 'mp'}, name='mp'),
    url(r'^group/$', list_detail.object_list, {'queryset': Group.objects.all()}, name='index_groups'),
    url(r'^group/(?P<object_id>.+)/$', list_detail.object_detail, {'queryset': Group.objects.all(), 'template_name': 'mps/container_detail.html'}, name='index_by_group'),
    url(r'^department/$', list_detail.object_list, {'queryset': Department.objects.all().order_by('number')}, name='index_departments'),
    url(r'^department/(?P<object_id>.+)/$', list_detail.object_detail, {'queryset': Department.objects.all(), 'template_name': 'mps/container_detail.html'}, name='index_by_department'),
)
