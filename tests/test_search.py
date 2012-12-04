from . import TestCase
from memopol.search.templatetags.search_tags import string_search_shortcut


class TestSearchTemplateTags(TestCase):

    def test_string_search_shortcut(self):
        url = string_search_shortcut('country:FR or country:BR')
        self.assertEqual(url, "/search/?s=country%3AFR%20or%20country%3ABR")
