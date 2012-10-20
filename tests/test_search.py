from . import TestCase
from memopol.search.templatetags.search_tags import simple_search_shortcut


class TestSearchTemplateTags(TestCase):

    def test_simple_search_shortcut(self):
        url = simple_search_shortcut('country:FR or country:BR')
        self.assertEqual(url, "/search/?q=country%3AFR%20or%20country%3ABR")
