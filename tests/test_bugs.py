from . import TestCase
from votes.models import Proposal


class TestAntiBugs(TestCase):

    def test_trends_of_strasser(self):
        self.app.get("/trends/mep/ErnstStrasser.png")

    def test_rss(self):
        self.app.get("/votes/latest/feed")

    def test_french_proposals_recommandation(self):
        id_of_a_recommendation_of_the_proposal = str(Proposal.objects.get(id="Loi_Hadopi_Assemblee_nationale").recommendation_set.all()[0].id)
        self.app.get("/france/assemblee/vote/Loi_Hadopi_Assemblee_nationale/" + id_of_a_recommendation_of_the_proposal + "/")

    def test_trends_french_proposal(self):
        self.app.get("/trends/proposal/groups-Loi_Hadopi_2_Assemblee_nationale-repartition-stacked.png")
        self.app.get("/trends/proposal/groups-Loi_Hadopi_Assemblee_nationale-repartition-heatmap.png")
