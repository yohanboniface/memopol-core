from django.db import models

class Vote(models.Model):
    id = models.CharField(max_length=63, primary_key=True)
    title = models.CharField(max_length=255, unique=True)
