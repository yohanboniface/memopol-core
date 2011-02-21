from django.db import models
from django.conf import settings

from couchdbkit import Server

class Mep(dict):
    """
    Our Mep pseudo model. Currently we use couchdbkit as a glorified http client and json parser,
    the objets we work with are just dicts. This is here to wrap things a little bit, and do our
    fixups (which should be moved to  the migration scripts anyway).
    
    FIXME - this is kind of fugly
    """
    def __init__(self, *args):
        dict.__init__(self, *args)
        self.fixup()
    
    def fixup(self):
        # fixup email.addr.text
        try:
            node = self["contact"]["email"]
            if not(type(node) is dict and node.has_key("text")):
                self["contact"]["email"] = { "text": node }
        except Exception:
            raise
    
    @staticmethod
    def get(key):
        couch = Server(settings.COUCHDB)
        return Mep(couch["meps"].get(key)) 


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
