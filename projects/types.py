from graphene_django import DjangoObjectType
from .models import Project

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'
