from django.views.generic import TemplateView

from votes.models import Proposal
from meps.models import Committee


class HomeView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        return {
            'proposals': Proposal.objects.filter(institution="EU")[:10],
            'committees': Committee.objects.order_by('abbreviation').all()
        }

home = HomeView.as_view()
