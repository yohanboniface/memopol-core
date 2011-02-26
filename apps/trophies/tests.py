from django.test import TestCase

from meps.models import MEP
from trophies.models import ManualTrophy, AutoTrophy, Reward

class ModelsTest(TestCase):
    def test_trophies_attribution(self):
        """
        Test that trophies' models can interact with CouchDB.
        """
        # Initialization
        a_mep = MEP.get('AlainLipietz')
        manual_trophy = ManualTrophy.objects.create(label="A manual trophy")
        auto_trophy = AutoTrophy.objects.create(label="An auto trophy")
        self.failUnlessEqual(a_mep.trophies, [])
        
        # Let's create a reward and attribute it to verify CouchDB's update
        reward = Reward.objects.create(mep_wikiname=a_mep._id, trophy=manual_trophy, reason="test")
        a_mep = MEP.get('AlainLipietz')
        self.failUnlessEqual(a_mep.trophies, [1])
        
        # OK, now we verify that deletion is triggered to CouchDB
        reward.delete()
        a_mep = MEP.get('AlainLipietz')
        self.failUnlessEqual(a_mep.trophies, [])
        

