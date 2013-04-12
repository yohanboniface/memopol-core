from django.views.generic import TemplateView

from memopol.votes.models import Proposal
from memopol.meps.models import Committee, MEP

from random import seed, randint
from datetime import datetime


class HomeView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Get a random mep

        # Old method
        # spotlight_mep = MEP.objects.filter(active=True).order_by("?")[0]

        # #415 : Make the "random MEP" the same for one day
        MEP_list = MEP.objects.filter(active=True)
        now = datetime.now()
        seed(int("{}{}{}".format(now.year, now.month, now.day)))
        spotlight_mep = MEP_list[randint(1,MEP_list.count())]

        return {
            'proposals': Proposal.objects.filter(institution="EU")[:10],
            'committees': Committee.objects.order_by('abbreviation').all(),
            'spotlight_mep': spotlight_mep
        }

home = HomeView.as_view()


class AboutView(TemplateView):
    template_name = "about.html"
about = AboutView.as_view()
