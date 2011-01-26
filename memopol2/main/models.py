from django.db import models
from memopol2 import settings

from couchdb import Server

class Mep(models.Model):
    couchid = models.CharField(primary_key=True, max_length=32)
    couch_data = None

    def load_couch_data(self):
        couch = Server(settings.COUCHDB)
        self.couch_data = couch["meps"][self.couchid]

    def get_couch_data(self):
        if self.couch_data is None:
            self.load_couch_data()
        return self.couch_data

    def __unicode__(self):
        return "<Mep id='%s'>" % self.couchid

class Position(models.Model):
    mep = models.ForeignKey(Mep)
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
