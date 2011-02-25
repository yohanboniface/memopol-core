from django.db import models

from couchdbkit.ext.django.schema import Document, StringProperty

class MEP(Document):
    id = StringProperty()

class Position(models.Model):
    mep_id = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    content = models.CharField(max_length=512)
    submitter_username = models.CharField(max_length=30)
    submitter_ip = models.IPAddressField()
    submit_datetime = models.DateTimeField()
    moderated = models.BooleanField()
    moderated_by = models.CharField(max_length=30)
    visible = models.BooleanField()

    def __json__(self):
        return {"mep_id": self.mep_id, "content": self.content}

    def __unicode__(self):
        return "<Position for mep id='%s'>" % (self.mep_id)
