from django.views.generic import TemplateView

from memopol.votes.models import Proposal
from memopol.meps.models import Committee, MEP


class HomeView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Get a random mep
        spotlight_mep = MEP.objects.filter(active=True).order_by("?")[0]
        return {
            'proposals': Proposal.objects.filter(institution="EU")[:10],
            'committees': Committee.objects.order_by('abbreviation').all(),
            'spotlight_mep': spotlight_mep
        }

home = HomeView.as_view()


class AboutView(TemplateView):
    template_name = "about.html"
about = AboutView.as_view()
