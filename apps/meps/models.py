from django.db import models

from couchdbkit.ext.django.schema import Document, StringProperty

class MEP(Document):
    id = StringProperty()

class Trophy(models.Model):
    label = models.TextField()
    logo = models.CharField(max_length=25) #name of associated logo

    def __unicode__(self):
        return len(self.label)>18 and foo[:15] + "..." or foo

    def __json__(self):
        return {"label": self.label, "logo": self.logo}


#Automatically attached to a MEP, with a condition
class TrophyAuto(Trophy):
    condition = models.TextField(default="def cond(mep): return False")  #python function, used in hasAchievement = eval(condition, {'mep': yourMepDocument})

    #Give achievement to mep if he deserves it
    def obtain(self, mep):
        hasAchievement = eval(self.condition, {'mep': mep})
        if hasAchievement:
            #Attach it to the user
            mep.achievement.append(self.id)
            MEP.save(mep)

            return hasAchievement


#Given by hand
class TrophyManual(Trophy):
    reason = models.TextField()

    def obtain(self, mep, reason="Because I want to!"):
        #We arbitrarly choose to give this trophy to a mep
        mep.achievement.append(self.id)
        MEP.save(mep)

        return true


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
