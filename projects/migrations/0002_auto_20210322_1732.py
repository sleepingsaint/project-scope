# Generated by Django 3.1.7 on 2021-03-22 17:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20210322_1115'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='blocked',
            field=models.ManyToManyField(blank=True, related_name='blocked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='blogs',
            field=models.ManyToManyField(blank=True, to='blogs.Blog'),
        ),
        migrations.AlterField(
            model_name='project',
            name='invites',
            field=models.ManyToManyField(blank=True, related_name='invites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='moderators',
            field=models.ManyToManyField(blank=True, related_name='moderators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='requests',
            field=models.ManyToManyField(blank=True, related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
    ]