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

class User_Validation(models.Model):
    task_id = models.CharField(max_length=512)
    user_id = models.CharField(max_length=512)
    time_stamp = models.TimeField((u"Time Stamp"), auto_now_add=True, blank=True)
    main_keyword = models.CharField(max_length=512)
    # Columns for related keywords tool
    relationship_keyword = models.CharField(max_length=512)
    relationship_is_related = models.IntegerField(default=-1)
    # Columns for domainnes tool
    domainnes_belongs_to_domain = models.IntegerField(default=-1)
