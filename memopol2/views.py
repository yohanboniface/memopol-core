from django.views.generic import TemplateView
from votes.models import Proposal


class HomeView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        return {
            'proposals': Proposal.objects.filter(institution="EU")[:5]
        }

home = HomeView.as_view()
