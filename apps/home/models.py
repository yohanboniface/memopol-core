from django.db import models

class Edito(models.Model):
    edito_title = models.CharField(max_length=128)
    edito = models.TextField()
