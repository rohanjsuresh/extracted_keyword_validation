# Generated by Django 3.0.8 on 2021-01-13 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Correct_Pairs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_fst', models.CharField(max_length=512)),
                ('keyword_snd', models.CharField(max_length=512)),
                ('correct_match_count', models.IntegerField(default=0)),
                ('incorrect_match_count', models.IntegerField(default=0)),
                ('times_classified', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Incorrect_Pairs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_fst', models.CharField(max_length=512)),
                ('keyword_snd', models.CharField(max_length=512)),
                ('correct_match_count', models.IntegerField(default=0)),
                ('incorrect_match_count', models.IntegerField(default=0)),
                ('times_classified', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword_Pages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=512)),
                ('matched_with', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='Pairs_In_Circulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_fst', models.CharField(max_length=512)),
                ('keyword_snd', models.CharField(max_length=512)),
                ('correct_match_count', models.IntegerField(default=0)),
                ('incorrect_match_count', models.IntegerField(default=0)),
                ('times_classified', models.IntegerField(default=0)),
            ],
        ),
    ]