from django.db import models

from couchdb import Server

class Mep(models.Model):
    couchid = models.CharField(primary_key=True, max_length=32)
    couch_data = None

    def load_couch_data(self):
        couch = Server("http://localhost:5984")
        self.couch_data = couch["meps"][self.couchid]

    def get_couch_data(self):
        if self.couch_data is None:
            self.load_couch_data()
        return self.couch_data

    def __unicode__(self):
        return "<Mep id='%s'>" % self.couchid

class Position(models.Model):
    mep = models.ForeignKey(Mep)
    content = models.CharField(max_length=200)
    submitter_username = models.CharField(max_length=30)
    submitter_ip = models.IPAddressField()
    submit_datetime = models.DateTimeField()
    moderated = models.BooleanField()
    visible = models.BooleanField()

    def __unicode__(self):
        return "<Position for mep id='%s'>" % (self.mep)
