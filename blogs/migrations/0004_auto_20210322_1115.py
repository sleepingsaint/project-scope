# Generated by Django 3.1.7 on 2021-03-22 11:15

import blogs.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_auto_20210320_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='more_info',
            field=models.JSONField(blank=True, default=blogs.models.default_more_info),
        ),
        migrations.AlterField(
            model_name='blog',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), blank=True, default=blogs.models.default_tags, size=None),
        ),
    ]
