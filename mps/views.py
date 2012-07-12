from urllib import urlopen
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import DetailView, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from models import MP, Phone, Address

def get_nosdeputes_widget(request, pk):
    mp = get_object_or_404(MP, id=pk)
    return HttpResponse(urlopen("http://www.nosdeputes.fr/widget/%s-%s" % (slugify(mp.first_name), slugify(mp.last_name))).read().replace("935", "800"))


class VoteRecommendation(DetailView):
    template_name='mps/recommendation_detail.html'
    redirect="mps:recommendation"

    def get_context_data(self, *args, **kwargs):
        context = super(VoteRecommendation, self).get_context_data(**kwargs)
        context['choice_listing'] = True
        context['proposal'] = self.object.proposal
        self.redirect_args = [self.object.proposal.id, self.object.id]
        return context

    def render_to_response(self, context):
        if self.kwargs["proposal_id"] != self.object.proposal.id:
            return HttpResponseRedirect(reverse(self.redirect, args=self.redirect_args))
        return DetailView.render_to_response(self, context)


class VoteRecommendationChoice(VoteRecommendation):
    template_name='mps/mp_list.html'
    redirect="mps:recommendation_choice"

    def get_context_data(self, *args, **kwargs):
        context = super(VoteRecommendationChoice, self).get_context_data(**kwargs)
        context['choice'] = self.kwargs['recommendation']
        context['header_template'] = 'votes/header_mep_list.html'
        context['object_list'] = MP.objects.filter(vote__recommendation=self.object,
                                  vote__choice=self.kwargs['recommendation'])
        self.redirect_args += [self.kwargs['recommendation']]
        return context


class MPList(ListView):
    queryset=MP.objects.filter(active=True)
    context_object_name="mp"

    def get_context_data(self, *args, **kwargs):
        context = super(MPList, self).get_context_data(**kwargs)
        optimize_mp_query(context["mp"])
        return context


class MPsFromModel(DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super(MPsFromModel, self).get_context_data(**kwargs)
        context["mps"] = optimize_mp_query(context["object"].mps)
        return context


def optimize_mp_query(query):
    query = query.select_related('group').prefetch_related("email_set")
    phones = {}
    for phone in Phone.objects.filter(type="phone", address__mp__active=True).select_related('address'):
        phones.setdefault(phone.address.id, []).append(phone)
    address = {}
    for addr in Address.objects.filter(mp__active=True).select_related('mp'):
        addr.phones = phones.get(addr.id, [])
        address.setdefault(addr.mp.id, []).append(addr)
    for mp in query:
        mp.address = address.get(mp.id, [])
    return query
