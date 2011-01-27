from django.db import models
from memopol2 import settings

from couchdbkit import *

class Mep(Document):
    # for compat with our silly views
    def get_couch_data(self):
        return self

# bind our couch db classes
couch_server = Server()
Mep.set_db(couch_server["meps"])
    
class Position(models.Model):
    mep = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    content = models.CharField(max_length=512)
    submitter_username = models.CharField(max_length=30)
    submitter_ip = models.IPAddressField()
    submit_datetime = models.DateTimeField()
    moderated = models.BooleanField()
    moderated_by = models.CharField(max_length=30)
    visible = models.BooleanField()

    def __json__(self):
        return {"mep_id": self.mep.couchid, "content": self.content}

    def __unicode__(self):
        return "<Position for mep id='%s'>" % (self.mep)
