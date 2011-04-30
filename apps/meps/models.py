from django.db import models

class Deleguation(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class Committe(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return u"%s: %s" % (self.abbreviation, self.name)

class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.name)

class Group(models.Model):
    abbreviation = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return u"%s - %s" % (self.abbreviation, self.name)

class Opinion(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.title
