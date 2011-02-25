from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class ViewsTest(TestCase):
    """
    Check basic context of mps' views.
    """
    def setUp(self):
        self.client = Client()

    def test_index(self):
        """
        Tests index context.
        """
        response = self.client.get(reverse("mps:index"))
        self.failUnlessEqual(len(response.context['mps']), 615)
        self.failUnlessEqual(repr(response.context['mps'].all()[0].name), "u'Abdoulatifou Aly'")

    def test_vote(self):
        """
        Tests detail context.
        """
        response = self.client.get(reverse("mps:detail", args=('AlainBocquet',)))
        self.failUnlessEqual(repr(response.context['mp'].name), "u'Alain Bocquet'")

