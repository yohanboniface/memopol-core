from django.db import models

class Function(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

class Opinion(models.Model):
    title = models.CharField(max_length=1023, unique=True)
    url = models.URLField()
    content = models.TextField()

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    number = models.CharField(max_length=3, primary_key=True)

    def count(self):
        return len(self.mps())

    def mps(self):
        return self.mp_set.filter(active=True)

class Circonscription(models.Model):
    number = models.CharField(max_length=31)
    department = models.ForeignKey(Department)

class Canton(models.Model):
    name = models.CharField(max_length=511)
    circonscription = models.ForeignKey(Circonscription)

class MP(models.Model):
    active = models.BooleanField()
    birth_department = models.CharField(max_length=255)
    an_id = models.IntegerField()
    an_speeches = models.URLField()
    an_debates = models.URLField(null=True)
    an_commissions = models.URLField()
    an_reports = models.URLField()
    an_questions = models.URLField()
    an_propositions = models.URLField()
    an_webpage = models.URLField()
    functions = models.ManyToManyField(Function, through='FunctionMP')
    profession = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department)

class FunctionMP(models.Model):
    mp = models.ForeignKey(MP)
    function = models.ForeignKey(Function)
    role = models.CharField(max_length=255)
    mission = models.CharField(max_length=255, null=True)


class Address(models.Model):
    key = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postcode = models.CharField(max_length=31)
    title = models.CharField(max_length=63, null=True)
    mp = models.ForeignKey(MP)

class Phone(models.Model):
    type = models.CharField(max_length=5, choices=((u'phone', u'Phone'), (u'fax', u'Fax')))
    number = models.CharField(max_length=63)
    address = models.ForeignKey(Address)

class Mandate(models.Model):
    current = models.BooleanField()
    type = models.CharField(max_length=127)
    role = models.CharField(max_length=255, null=True)
    election_date = models.DateField(null=True)
    begin_term = models.DateField(null=True)
    begin_reason = models.CharField(max_length=255, null=True)
    end_term = models.DateField(null=True)
    end_reason = models.CharField(max_length=255, null=True)
    institution = models.CharField(max_length=255, null=True)
    mp = models.ForeignKey(MP)
