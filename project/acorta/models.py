from django.db import models

# Create your models here.

class Url(models.Model):

    long_url = models.CharField(max_length=64) 
    #url_corta = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.long_url
