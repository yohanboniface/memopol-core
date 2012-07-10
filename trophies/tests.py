from django.test import TestCase

from meps.models import MEP
from trophies.models import ManualTrophy, AutoTrophy, Reward

class ModelsTest(TestCase):
    def setUp(self):
        # Delete all trophies for the test user
        a_mep = MEP.get('AlainLipietz')
        a_mep.trophies_ids = []
        a_mep.save()
    
    tearDown = setUp
    
    def test_trophies_attribution(self):
        """
        Test that trophies' models can interact with CouchDB.
        """
        # Initialization
        a_mep = MEP.get('AlainLipietz')
        manual_trophy = ManualTrophy.objects.create(label="A manual trophy")
        auto_trophy = AutoTrophy.objects.create(label="An auto trophy")
        self.failUnlessEqual(a_mep.trophies_ids, [])
        
        # Let's create a reward and attribute it to verify CouchDB's update
        reward = Reward.objects.create(mep_wikiname=a_mep._id, trophy=manual_trophy, reason="test")
        a_mep = MEP.get('AlainLipietz')
        self.failUnlessEqual(a_mep.trophies_ids, [1])
        
        # OK, now we verify that deletion is triggered to CouchDB
        reward.delete()
        a_mep = MEP.get('AlainLipietz')
        self.failUnlessEqual(a_mep.trophies_ids, [])
        

    def test_trophies_retrieval_from_mep(self):
        """
        Test that meps' CouchDB model can retrieve associated Django trophies.
        """
        # Initialization
        a_mep = MEP.get('AlainLipietz')
        manual_trophy = ManualTrophy.objects.create(label="A manual trophy")
        auto_trophy = AutoTrophy.objects.create(label="An auto trophy")
        self.failUnlessEqual(a_mep.trophies, [])
        
        # Let's create a reward and attribute it to verify CouchDB's update
        reward = Reward.objects.create(mep_wikiname=a_mep._id, trophy=manual_trophy, reason="test")
        a_mep = MEP.get('AlainLipietz')
        self.failUnlessEqual(repr(a_mep.trophies), "[<ManualTrophy: A manual trophy>]")
        
        # OK, now we verify that deletion is triggered to CouchDB
        reward.delete()
        a_mep = MEP.get('AlainLipietz')
        self.failUnlessEqual(a_mep.trophies, [])
        
