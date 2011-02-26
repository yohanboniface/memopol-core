from django.db import models

from couchdbkit.ext.django.schema import Document, StringProperty

class MEP(Document):
    id = StringProperty()


#The fact that MEP is a Document messes with the traditional django relationships
class Trophy(models.Model):
    label = models.TextField()
    logo = models.CharField(max_length=25) #name of associated logo

    def __unicode__(self):
        return len(self.label)>18 and self.label[:15] + "..." or self.label

    def __json__(self):
        return {"label": self.label, "logo": self.logo}


#Automatically attached to a MEP, with a condition
class AutoTrophy(Trophy):
    condition = models.TextField(default="False")  #python function, used in hasAchievement = eval(condition, {'mep': yourMepDocument})

    #Give achievement to mep if he deserves it
    def obtain(self, mep):
        hasAchievement = eval(self.condition, {'mep': mep})
        if hasAchievement:
            #Attach it to the user
            mep.achievement.append(self.id)
            mep.save()

            return hasAchievement


#Given by hand
class ManualTrophy(Trophy):

    def obtain(self, mep, reason="Because I want to!"):
        #We arbitrarly choose to give this trophy to a mep
        mep.achievement.append(self.id)
        mep.save()

        return true

#Representation of the many-to-many relationship
class Reward(models.Model):
    mep = models.IntegerField() #Id of the MEP
    trophy = models.ForeignKey(Trophy)
    date_attribution = models.DateField()
    reason_attribution = models.TextField() #Shall be null if the Trophy is auto



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
