import graphene
from .types import UserType, UserStatusType
from .models import CustomUser as User
from graphql_auth.models import UserStatus
from graphql_auth import mutations
from blogs.types import BlogType

class AuthQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    status = graphene.Field(UserStatusType, id=graphene.ID(required=True))

    whoami = graphene.Boolean()

    def resolve_whoami(parent, info):
        return info.context.user.is_authenticated
        
    def resolve_users(parent, info):
        return User.objects.all()

    def resolve_user(parent, info, id):
        return User.objects.get(pk=id)

    def resolve_status(parent, info, id):
        return UserStatus.objects.get(pk=id)

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
