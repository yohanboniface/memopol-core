from tests import TestCase
from meps.models import MEP

class TestAntiBugs(TestCase):

    def test_trends_of_strasser(self):
        self.app.get("/trends/mep/ErnstStrasser.png")

    def test_rss(self):
        self.app.get("/votes/latest/feed")
