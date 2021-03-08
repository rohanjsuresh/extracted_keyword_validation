from django.db import models

# Create your models here.

class Definitions_In_Circulation(models.Model):
    keyword = models.CharField(max_length=512)
    candidate_definition = models.CharField(max_length=4098)
    times_classified = models.IntegerField(default=0)