from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class ViewsTest(TestCase):
    """
    Check basic context of indexes' views.
    """
    def setUp(self):
        self.client = Client()
