from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import CustomUser as User
from blogs.models import Blog

# Create your models here.
def default_tags():
    return []

class Project(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=20), blank=True, default=default_tags)

    moderators = models.ManyToManyField(User, related_name="moderators", blank=True)
    members = models.ManyToManyField(User, related_name="members", blank=True)

    invites = models.ManyToManyField(User, related_name="invites", blank=True)
    requests = models.ManyToManyField(User, related_name="requests", blank=True)
    blocked = models.ManyToManyField(User, related_name="blocked", blank=True)

    blogs = models.ManyToManyField(Blog, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    repository = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title 