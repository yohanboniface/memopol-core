from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class ViewsTest(TestCase):
    """
    Check basic context of votes' views.
    """
    def setUp(self):
        self.client = Client()

    def test_index(self):
        """
        Tests index context.
        """
        response = self.client.get(reverse("votes:index"))
        self.failUnlessEqual(len(response.context['votes']), 7)
        self.failUnlessEqual(repr(response.context['votes'].all()[0].label), 'u\'Directive sur la brevetabilit\\xe9 des "inventions mise en \\u0153uvre par ordinateur" (brevets logiciels), 1re lecture\'')

    def test_detail(self):
        """
        Tests detail context.
        """
        response = self.client.get(reverse("votes:detail", args=('Directive_brevets_logiciels_1re_lecture',)))
        self.failUnlessEqual(repr(response.context['vote'].label), 'u\'Directive sur la brevetabilit\\xe9 des "inventions mise en \\u0153uvre par ordinateur" (brevets logiciels), 1re lecture\'')
