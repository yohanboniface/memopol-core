from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class ViewsTest(TestCase):
    """
    Check basic context of indexes' views.
    """
    def setUp(self):
        self.client = Client()

    def test_index_names(self):
        """
        Tests index_names context.
        """
        response = self.client.get(reverse("meps:index_names"))
        self.failUnlessEqual(len(response.context['meps']), 1194)
        self.assertTrue(u"ECR" in [i.group for i in response.context['meps']])
        a = response.context['meps'].all()[:2]
        self.assertTrue(a[0].last[0] < a[1].last[1])

    def test_index_groups(self):
        """
        Tests index_groups context.
        """
        response = self.client.get(reverse("meps:index_groups"))
        self.failUnlessEqual(len(response.context['groups']), 12)
        self.failUnlessEqual(repr(response.context['groups'][0]), "{u'value': {u'count': 268, u'name': u'Groupe du Parti Populaire Europ\\xe9en (D\\xe9mocrates-Chr\\xe9tiens)'}, u'key': u'PPE'}")
        
    def test_index_countries(self):
        """
        Tests index_countries context.
        """
        response = self.client.get(reverse("meps:index_countries"))
        self.failUnlessEqual(len(response.context['countries']), 27)
        self.failUnlessEqual(repr(response.context['countries'][0]), "{u'value': {u'count': 141, u'name': u'Allemagne'}, u'key': u'DE'}")

    def test_index_by_country(self):
        """
        Tests index_by_country context.
        """
        response = self.client.get(reverse("meps:index_by_country", args=('DE',)))
        self.failUnlessEqual(len(response.context['meps']), 141)
        self.failUnlessEqual(response.context['meps'].first().group, u"PPE")
        self.failUnlessEqual(response.context['meps'].first().first, u"Albert")

    def test_index_by_group(self):
        """
        Tests index_by_group context.
        """
        response = self.client.get(reverse("meps:index_by_group", args=('ALDE',)))
        self.failUnlessEqual(len(response.context['meps']), 144)
        self.failUnlessEqual(response.context['meps'].first().group, u"ALDE")
        self.failUnlessEqual(response.context['meps'].first().first, u"Adina-Ioana")

    def test_mep(self):
        """
        Tests mep context.
        """
        response = self.client.get(reverse("meps:mep", args=('AlbertDess',)))
        self.failUnlessEqual(repr(response.context['mep']['cv']['position'][-1]), 'u"M\\xe9daill\\xe9 de l\'ordre bavarois du M\\xe9rite (2007)."')
        self.failUnlessEqual(str(response.context['mep']['contact']['address'][0]['street']), '60, rue Wiertz')
        self.failUnlessEqual(repr(response.context['positions']), "[]")
        self.failUnlessEqual(repr(response.context['visible_count']), "0")

    def test_js_functionnal_test(self):
        """
        Test the functionnal test that allow to make the js fail
        """
        from django.conf import settings
        settings.DEBUG = True
        response = self.client.get(reverse("meps:mep_addposition", args=('AlbertDess',)), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.failUnlessEqual(response.content, '{"success": true}')

    def test_js_functionnal_test_make_fail(self):
        """
        Test the functionnal test that allow to make the js fail
        """
        from django.conf import settings
        settings.DEBUG = True
        response = self.client.get(reverse("meps:mep_addposition", args=('AlbertDess',)), {'text' : 'fail'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.failUnlessEqual(response.content, '{"success": false}')
