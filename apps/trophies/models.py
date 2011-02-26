from django.db import models
from django.db.models.signals import post_save, pre_delete

from meps.models import MEP

def retrieve_meps_choices():
    """
    Dynamically retrieve MEPs ids from CouchDB to propose choices in Django.
    """
    meps = MEP.view('meps/all')
    return ((mep.id, mep.doc['infos']['name']['full']) for mep in meps)


class ManualTrophy(models.Model):
    """
    A trophy manually attributed by an admin through administration interface.
    
    A trophy is a way to flag a MEP with a label/logo.
    """
    label = models.TextField()
    logo = models.ImageField(blank=True, null=True, upload_to='logos')
    
    def __unicode__(self):
        return len(self.label)>18 and self.label[:15] + "..." or self.label

    def __json__(self):
        return {"label": self.label, "logo": self.logo}

    def attribute_to(self, mep):
        """
        Attribute the trophy to the mep parameter.
        """
        mep.trophies_ids.append(self.id)
        mep.save()

    def discharge_to(self, mep):
        """
        Discharge the trophy to the mep parameter.
        """
        mep.trophies_ids.remove(self.id)
        mep.save()


class AutoTrophy(ManualTrophy):
    """
    A trophy dynamically attributed by computation, depends on a condition.
    """
    condition = models.TextField(default="False", help_text="python function, used in attribute_to = eval(condition, {'mep': mep}")

    def attribute_to(self, mep):
        """
        Attribute the trophy to the mep parameter given the model's condition.
        """
        if eval(self.condition, {'mep': mep}):
            # Attach it to the user
            mep.trophies_ids.append(self.id)
            mep.save()


class Reward(models.Model):
    """
    Representation of the M2M relationship between SQL and CouchDB.
    """
    mep_wikiname = models.CharField(max_length=255, 
                                    choices=retrieve_meps_choices(),
                                    help_text='Retrieved from CouchDB')
    trophy = models.ForeignKey(ManualTrophy)
    date = models.DateField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return u'"%s" attributed to %s%s' % (self.trophy, self.mep_wikiname,
            self.reason and u' because "%s"' % self.reason)

    @property
    def mep(self):
        return MEP.get(self.mep_wikiname)

def update_trophies_addition(sender, **kwargs):
    if kwargs['created']:
        kwargs['instance'].trophy.attribute_to(kwargs['instance'].mep)

def update_trophies_removal(sender, **kwargs):
    kwargs['instance'].trophy.discharge_to(kwargs['instance'].mep)

post_save.connect(update_trophies_addition, sender=Reward)
pre_delete.connect(update_trophies_removal, sender=Reward)

