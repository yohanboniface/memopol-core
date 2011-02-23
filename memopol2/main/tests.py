from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class ViewsTest(TestCase):
    """
    Check basic context of indexes' views.
    """
    def test_index_names(self):
        """
        Tests index_names context.
        """
        client = Client()
        response = client.get(reverse("index_names"))
        self.failUnlessEqual(len(response.context['meps_list']), 1194)
        self.failUnlessEqual(repr(response.context['meps_list'][0]), "{u'value': {u'group': u'ECR', u'last': u'Bielan', u'first': u'Adam'}, u'id': u'AdamBielan', u'key': None}")

    def test_index_groups(self):
        """
        Tests index_groups context.
        """
        client = Client()
        response = client.get(reverse("index_groups"))
        self.failUnlessEqual(len(response.context['groups']), 12)
        self.failUnlessEqual(repr(response.context['groups'][0]), '{u\'value\': {u\'count\': 144, u\'name\': u"Groupe Alliance des d\\xe9mocrates et des lib\\xe9raux pour l\'Europe"}, u\'key\': u\'ALDE\'}')

    def test_index_countries(self):
        """
        Tests index_countries context.
        """
        client = Client()
        response = client.get(reverse("index_countries"))
        self.failUnlessEqual(len(response.context['countries']), 27)
        self.failUnlessEqual(repr(response.context['countries'][0]), "{u'value': {u'count': 141, u'code': u'DE'}, u'key': u'Allemagne'}")

    def test_index_by_country(self):
        """
        Tests index_by_country context.
        """
        client = Client()
        response = client.get(reverse("index_by_country", args=('DE',)))
        self.failUnlessEqual(len(response.context['meps_list']), 141)
        self.failUnlessEqual(repr(response.context['meps_list'][0]), "{u'value': {u'group': u'PPE', u'last': u'Dess', u'first': u'Albert'}, u'id': u'AlbertDess', u'key': u'DE'}")

    def test_index_by_group(self):
        """
        Tests index_by_group context.
        """
        client = Client()
        response = client.get(reverse("index_by_group", args=('ALDE',)))
        self.failUnlessEqual(len(response.context['meps_list']), 144)
        self.failUnlessEqual(repr(response.context['meps_list'][0]), "{u'value': {u'group': u'ALDE', u'last': u'V\\u0103lean', u'first': u'Adina-Ioana'}, u'id': u'AdinaIoanaValean', u'key': u'ALDE'}")

    def test_mep(self):
        """
        Tests mep context.
        """
        client = Client()
        response = client.get(reverse("mep", args=('AlbertDess',)))
        self.failUnlessEqual(repr(response.context['d'].keys()), "[u'activities', u'functions', u'_rev', u'extid', u'contact', u'scores', u'infos', u'_id', u'cv']")
        self.failUnlessEqual(repr(response.context['d']['cv']['position'][-1]), 'u"M\\xe9daill\\xe9 de l\'ordre bavarois du M\\xe9rite (2007)."')
        self.failUnlessEqual(str(response.context['d']['contact']['address'][0]['street']), '60, rue Wiertz')
        self.failUnlessEqual(repr(response.context['positions']), "[]")

