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
    wiki_definition = models.CharField(max_length=4096, default="")
    google_graph_embedding = models.CharField(max_length=4096, default="")
    wiki_path = models.CharField(max_length=2048, default="")

class User_Validation(models.Model):
    task_id = models.CharField(max_length=512)
    user_id = models.CharField(max_length=512)
    time_stamp = models.TimeField((u"Time Stamp"), auto_now_add=True, blank=True)
    main_keyword = models.CharField(max_length=512)
    # Columns for related keywords tool
    relationship_keyword = models.CharField(max_length=512)
    relationship_is_related = models.IntegerField(default=-1)
    # Columns for domainnes tool
    domainness_belongs_to_domain = models.IntegerField(default=-1)
    # Columns for definition tool
    definition_is_def_valid = models.IntegerField(default=-1)
    definition_candidate_definition = models.CharField(max_length=4096, default="N/A")

class User_Validation_Summary(User_Validation):
    class Meta:
        proxy = True
        verbose_name = "User Validation Summary"
        verbose_name_plural = "Users Validation Summary"