from graphene_django import DjangoObjectType
from .models import Blog
import graphene

class BlogType(DjangoObjectType):
    class Meta:
        model = Blog
        fields = '__all__'

class BlogInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    data = graphene.String()
    tags = graphene.List(graphene.String)
    more_info = graphene.JSONString()