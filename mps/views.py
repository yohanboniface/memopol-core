from urllib import urlopen
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import DetailView, ListView
from django.db.models import Q

from models import MP, Phone, Address

def get_nosdeputes_widget(request, pk):
    mp = get_object_or_404(MP, id=pk)
    if mp.active:
        return HttpResponse(urlopen("http://www.nosdeputes.fr/widget14/%s-%s" % (slugify(mp.first_name), slugify(mp.last_name))).read().replace("935", "800"))
    else:
        return HttpResponse(urlopen("http://www.nosdeputes.fr/widget/%s-%s" % (slugify(mp.first_name), slugify(mp.last_name))).read().replace("935", "800"))


class MPList(ListView):
    queryset=MP.objects.filter(active=True)
    context_object_name="mps"

    def get_context_data(self, *args, **kwargs):
        context = super(MPList, self).get_context_data(**kwargs)
        context["mps"] = optimize_mp_query(context["mps"], Q(mp__active=True), Q(address__mp__active=True))
        return context


class MPsFromModel(DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super(MPsFromModel, self).get_context_data(**kwargs)
        context["mps"] = optimize_mp_query(context["object"].mps, *context["object"].q_objects)
        return context


class MPView(DetailView):
    queryset=MP.objects.select_related('group', 'department')
    context_object_name='mp'

    def get_context_data(self, *args, **kwargs):
        context = super(MPView, self).get_context_data(**kwargs)
        context["mp"].scores_optimized = context["mp"].score_set.select_related('proposal')
        context["mp"].functions_optimized = context["mp"].functionmp_set.select_related('function')
        context["mp"].opinions_optimized = context["mp"].opinionrep_set.select_related('opinion')
        context["mp"].address_optimized = context["mp"].address_set.prefetch_related('phone_set')
        return context


def optimize_mp_query(query, q_object=Q(), q_object_address=Q()):
    query = query.select_related('group').prefetch_related("email_set")
    phones = {}
    for phone in Phone.objects.filter(type="phone").filter(q_object_address).select_related('address'):
        phones.setdefault(phone.address.id, []).append(phone)
    address = {}
    for addr in Address.objects.filter(q_object).select_related('mp'):
        addr.phones = phones.get(addr.id, [])
        address.setdefault(addr.mp.id, []).append(addr)
    for mp in query:
        mp.address = address.get(mp.id, [])
    return query
