from django.db import models
from couchdbkit import Server
from memopol2 import settings


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

class Database(object):
    def __init__(self):
        self.couch = Server(settings.COUCHDB)

    def get_groups(self):
        map_fun = """
        function(d) {
            emit(d.infos.group.abbreviation, { name: d.infos.group.name,  count: 1 });
        }
        """

        reduce_fun = """function(keys, values) {
            var sum = 0;
            for (var idx in values)
            {
                sum += values[idx].count;
            }
            return {name: values[0].name , count: sum};
        }"""

        couch_meps = self.couch["meps"]
        groups = couch_meps.temp_view({"map": map_fun, "reduce": reduce_fun}, group=True)
        groups.fetch()
        return groups.all()

    def get_countries(self):
        map_fun = """
        function(d) {
            emit(d.infos.constituency.country.name, { code: d.infos.constituency.country.code, count: 1 });
        }
        """

        reduce_fun = """function(keys, values) {
            var sum = 0;
            for (var idx in values)
            {
                sum += values[idx].count;
            }
            return {code: values[0].code, count: sum};
        }"""

        couch_meps = self.couch["meps"]

        req = couch_meps.temp_view({"map": map_fun, "reduce": reduce_fun }, group=True)
        req.fetch()
        return req.all()

    def get_meps_by_names(self):
        return self._get_meps()

    def get_meps_by_country(self, country_code):
        return self._get_meps(country_code.upper(), "infos.constituency.country.code")

    def get_meps_by_group(self, group):
        return self._get_meps(group, "infos.group.abbreviation")

    def _get_meps(self, key=None, couch_key=None):

        map_fun = "function(d) {"

        if couch_key:
            map_fun += """
                if (d.%s)
                {
                    emit(d.%s, {first: d.infos.name.first, last: d.infos.name.last, group: d.infos.group.abbreviation});
                }
                """ % (couch_key, couch_key)
        else:
            map_fun += "emit(null, {first: d.infos.name.first, last: d.infos.name.last, group: d.infos.group.abbreviation});"

        map_fun += "}"

        couch_meps = self.couch["meps"]
        req = couch_meps.temp_view({"map": map_fun}, key=key)
        req.fetch()
        return req.all()
