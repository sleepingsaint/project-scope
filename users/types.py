from .models import CustomUser as User
from graphql_auth.models import UserStatus
from graphene_django.types import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ('password',)

class UserStatusType(DjangoObjectType):
    class Meta:
        model = UserStatus
        fields = '__all__'