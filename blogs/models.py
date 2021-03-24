from django.db import models
from users.models import CustomUser as User
from django.contrib.postgres.fields import ArrayField

# Create your models here

def default_tags():
    return []

def default_more_info():
    return {}

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    data = models.TextField()
    tags = ArrayField(models.CharField(max_length=30), default=default_tags, blank=True, null=True)
    more_info = models.JSONField(default=default_more_info, blank=True, null=True)

    is_project_blog = models.BooleanField(default=False)

    def __str__(self):
        return self.title