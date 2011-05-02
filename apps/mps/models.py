from django.db import models

class Function(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

class Opinion(models.Model):
    title = models.CharField(max_length=1023, unique=True)
    url = models.URLField()
    content = models.TextField()

class MP(models.Model):
    active = models.BooleanField()
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=2, choices=((u'M', u'Male'), (u'F', u'Female')))
    picture = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField()
    birth_city = models.CharField(max_length=255)
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

class FunctionMP(models.Model):
    mp = models.ForeignKey(MP)
    function = models.ForeignKey(Function)
    role = models.CharField(max_length=255)
    mission = models.CharField(max_length=255, null=True)
