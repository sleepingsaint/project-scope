import graphene
from .types import BlogType
from .models import Blog
from users.models import CustomUser as User
import json

class BlogQuery(graphene.ObjectType):
    blogs = graphene.List(BlogType)
    blog = graphene.Field(BlogType, id=graphene.ID(required=True))
    user_blogs = graphene.List(BlogType, id=graphene.ID(required=True))

    def resolve_blogs(parent, info):
        return Blog.objects.all()
    
    def resolve_blog(parent, info, id):
        return Blog.objects.get(pk=id)

    def resolve_user_blogs(parent, info, id):
        author = User.objects.get(pk=id)
        return Blog.objects.filter(author=author)
        
class CreateBlogMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        data = graphene.String(required=True)
        tags = graphene.List(graphene.String)
        more_info = graphene.JSONString()
    
    blog = graphene.Field(BlogType)

    @classmethod
    def mutate(cls, root, info, title, data, tags, more_info):
        user = info.context.user
        if(user.is_authenticated):
            author = User.objects.get(pk=user.id)
            blog = Blog(author=author, title=title, data=data, tags=tags, more_info=more_info)
            blog.save()
            return CreateBlogMutation(blog=blog)

        raise Exception("You need to login to access the api")

class UpdateBlogMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=False)
        data = graphene.String(required=False)
        tags = graphene.List(graphene.String, required=False)
        more_info = graphene.JSONString(required=False)
    
    blog = graphene.Field(BlogType)

    @classmethod
    def mutate(cls, root, info, id, title=None, data=None, tags=None, more_info=None):
        user = info.context.user

        if(user.is_authenticated):
            blog = Blog.objects.get(pk=id)
            
            if(blog.is_project_blog):
                raise Exception("This action is forbid on this endpoint.")
            if(blog.author == user):
                if title is not None:
                    blog.title = title
                
                if data is not None:
                    blog.data = data

                if tags is not None:
                    blog.tags = tags
                
                if more_info is not None:
                    blog.more_info = more_info

                blog.save()
                return UpdateBlogMutation(blog=blog)
            raise Exception("You don't have permissions to perform this operation")
        raise Exception("You have to be logged in to access api")

class DeleteBlogMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    response = graphene.JSONString()

    @classmethod
    def mutate(cls, root, info, id):
        user = info.context.user

        if(user.is_authenticated):
            blog = Blog.objects.get(pk=id)
            if(blog.is_project_blog):
                raise Exception("This action is forbid on this endpoint.")
            if(blog.author == user):
                blog.delete()
                response = {
                    "success": True,
                    "error": False
                }
                return DeleteBlogMutation(response=json.dumps(response))
            raise Exception("You don't have permissions to perform this operation")
        raise Exception("You have to logged in to access api")
