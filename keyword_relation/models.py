from django.db import models

# Create your models here.

class Pairs_In_Circulation(models.Model):
    keyword_fst = models.CharField(max_length=512)
    keyword_snd = models.CharField(max_length=512)
    correct_match_count = models.IntegerField(default=0)
    incorrect_match_count = models.IntegerField(default=0)
    times_classified = models.IntegerField(default=0)

class Correct_Pairs(models.Model):
    keyword_fst = models.CharField(max_length=512)
    keyword_snd = models.CharField(max_length=512)
    correct_match_count = models.IntegerField(default=0)
    incorrect_match_count = models.IntegerField(default=0)
    times_classified = models.IntegerField(default=0)

class Incorrect_Pairs(models.Model):
    keyword_fst = models.CharField(max_length=512)
    keyword_snd = models.CharField(max_length=512)
    correct_match_count = models.IntegerField(default=0)
    incorrect_match_count = models.IntegerField(default=0)
    times_classified = models.IntegerField(default=0)

class Keyword_Pages(models.Model):
    keyword = models.CharField(max_length=512)
    matched_with = models.CharField(max_length=2048)