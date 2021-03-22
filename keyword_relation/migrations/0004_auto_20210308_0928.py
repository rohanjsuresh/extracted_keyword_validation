# Generated by Django 3.0.8 on 2021-03-08 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_relation', '0003_user_validation_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_validation',
            old_name='domainnes_belongs_to_domain',
            new_name='domainness_belongs_to_domain',
        ),
        migrations.AddField(
            model_name='user_validation',
            name='definition_candidate_definition',
            field=models.CharField(default='N/A', max_length=4096),
        ),
        migrations.AddField(
            model_name='user_validation',
            name='definition_is_def_valid',
            field=models.IntegerField(default=-1),
        ),
    ]