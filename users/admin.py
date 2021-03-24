from django.contrib import admin
from .models import CustomUser as User
from django.apps import apps
from django.contrib.auth.admin import UserAdmin

models = apps.get_app_config('graphql_auth').models.items()

for model_name, model in models:
    admin.site.register(model)

admin.site.register(User, UserAdmin)