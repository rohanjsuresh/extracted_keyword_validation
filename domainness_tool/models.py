from django.db import models

# Create your models here.

class Domainness_Match(models.Model):
    keyword = models.CharField(max_length=512)
    positive_count = models.IntegerField(default=0)
    negative_match_count = models.IntegerField(default=0)
