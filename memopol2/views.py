from django.views.generic import TemplateView


class HomeView(TemplateView):

    template_name = "home.html"

home = HomeView.as_view()
