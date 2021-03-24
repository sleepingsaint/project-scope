import graphene
from .models import Project
from .types import ProjectType
from users.models import CustomUser as User
import json
from blogs.types import BlogInputType, BlogType
from blogs.models import Blog

class ProjectQuery(graphene.ObjectType):
    projects = graphene.List(ProjectType)
    project = graphene.Field(ProjectType, id=graphene.ID(required=True))

    def resolve_projects(parent, info):
        return Project.objects.all()
    
    def resolve_project(parent, info, id):
        return Project.objects.get(pk=id)


class CreateProjectMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String(required=False)
        tags = graphene.List(graphene.String, required=False)
    
    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, title, description=None, tags=None):
        user = info.context.user
        if(user.is_authenticated):
            admin = User.objects.get(pk=user.id)
            project = Project(admin=admin, title=title)

            if description is not None:
                project.description = description
            
            if tags is not None:
                project.tags = tags

            project.save()

            return CreateProjectMutation(project=project)

        raise Exception("You need to login to access the api")

class UpdateProjectMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=False)
        description = graphene.String(required=False)
        tags = graphene.List(graphene.String, required=False)
        repository = graphene.String()

    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, id, title=None, description=None, tags=None, repository=None):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=id)
            if(project.admin.id == user.id):
                if title is not None:
                    project.title = title
                
                if description is not None:
                    project.description = description

                if tags is not None:
                    project.tags = tags

                if repository is not None:
                    project.repository = repository

                project.save()
                return UpdateProjectMutation(project=project)
            
            raise Exception("You don't have permissions to perform this action")
        raise Exception("You need to be logged in to access the api")

class DeleteProjectMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    response = graphene.JSONString()

    @classmethod
    def mutate(cls, root, info, id):
        user = info.context.user

        if(user.is_authenticated):
            project = Project.objects.get(pk=id)
            if(project.admin.id == user.id):
                project.delete()
                response = {
                    "success": True,
                    "error": False
                }
                return DeleteProjectMutation(response=json.dumps(response))
            raise Exception("You don't have permissions to perform this operation")
        raise Exception("You have to logged in to access api")


# send invites
# wrong implementation for invites
# invite will be a link 
# which redirect to send request link

# send request
class SendRequestMutation(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, project_id):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            requesting_user = User.objects.get(pk=user_id)
            
            if(requesting_user in projectj.members or requesting_user in project.moderators or requesting_user.id == project.admin.id):
                status = "You are already a member of the project!"
                return SendRequestMutation(status=status)

            if(requesting_user not in project.requests or requesting_user not in project.blocked):
                project.requests.add(requesting_user)
                project.save()
                status = "Request Sent :)"
                return SendRequestMutation(status=status)
            
            status = "Request already sent!"
            return SendRequestMutation(status=status)

        raise Exception("You have to logged in to access api")

# accept requrest
class AcceptRequestMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        project_id = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, project_id):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            if(project.admin.id == user.id or user in project.moderators):
                requesting_user = User.objects.get(pk=user_id)
                if requesting_user in project.requests:
                    project.requests.remove(requesting_user)
                    project.members.add(requesting_user)
                    project.save()
                    status = "Request Accepted :)"
                    return AcceptRequestMutation(status=status)
                else:
                    raise Exception("Request doesn't exist")
            raise Exception("You don't have permissions to perform this action")
        raise Exception("You have to logged in to access api")

# decline request
class DeclineRequestMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        project_id = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, project_id):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            if(project.admin.id == user.id or user in project.moderators):
                requesting_user = User.objects.get(pk=user_id)
                if requesting_user in project.requests:
                    project.requests.remove(requesting_user)
                    project.save()
                    status = "Request Declined!"
                    return DeclineRequestMutation(status=status)
                else:
                    raise Exception("Request doesn't exist")
            raise Exception("You don't have permissions to perform this operation")
        raise Exception("You have to logged in to access api")

# make moderator
class MakeModeratorMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        project_id = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, project_id):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            if(project.admin.id == user.id):
                
                requesting_user = User.objects.get(pk=user_id)
                if requesting_user in project.members:
                    project.moderators.add(requesting_user)
                    project.members.remove(requesting_user)
                    project.save()
                    status = "Added Moderator Designation!"
                    return MakeModeratorMutation(status=status)
                else:
                    raise Exception("Requested user is not a member of the project")
            raise Exception("You don't have permissions to perform this operation")
        raise Exception("You have to logged in to access api")

# remove from moderator
class RemoveModeratorMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        project_id = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, project_id):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            if(project.admin.id == user.id):
                requesting_user = User.objects.get(pk=user_id)
                if requesting_user in project.moderators:
                    project.moderators.remove(requesting_user)
                    project.members.add(requesting_user)
                    project.save()
                    status = "Removed Moderator Designation!"
                    return RemoveModeratorMutation(status=status)
                else:
                    raise Exception("Requested user is not a moderator")
            raise Exception("You don't have permissions to perform this operation")
        raise Exception("You have to logged in to access api")


# delete member
class DeleteMemberMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        project_id = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, project_id):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            requesting_user = User.objects.get(pk=user_id)
            status = None
            if(requesting_user in project.moderators):
                if(project.admin.id == user.id):
                    project.moderators.remove(requesting_user)
                    project.save()
                    status = "User Removed successfully"
                else:
                    raise Exception("You don't have permissions to perform this operation")
            elif requesting_user in project.members:
                if(project.admin.id == user.id or user in project.moderators):
                    project.members.remove(requesting_user)
                    project.save()
                    status = "User Removed successfully!"
                else:  
                    raise Exception("You don't have permissions to perform this operation")
            else:
                raise Exception("Requested user is not a member of the project")
            return DeleteProjectMutation(status=status)
        raise Exception("You have to logged in to access api")

# block member
class BlockMemberMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        project_id = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, project_id):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            requesting_user = User.objects.get(pk=user_id)

            status = None
            if(requesting_user in project.moderators):
                if(project.admin.id == user.id):
                    project.moderators.remove(requesting_user)
                    project.blocked.add(requesting_user)
                    project.save()
                    status = "User Blocked"
                else:
                    raise Exception("You don't have permissions to perform this operation")
            elif requesting_user in project.members:
                if(project.admin.id == user.id or user in project.moderators):
                    project.members.remove(requesting_user)
                    project.blocked.add(requesting_user)
                    project.save()
                    status = "User Blocked successfully!"
                else:  
                    raise Exception("You don't have permissions to perform this operation")
            else:
                raise Exception("Requested user is not a member of the project")
            return BlockMemberMutation(status=status)
        raise Exception("You have to logged in to access api")

# unblock member
class UnBlockMemberMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        project_id = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def mutate(cls, root, info, user_id, project_id):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            requesting_user = User.objects.get(pk=user_id)

            status = None
            if(requesting_user in project.blocked):
                if(project.admin.id == user.id or user in project.moderators):
                    project.blocked.remove(requesting_user)
                    project.save()
                    status = "User unblocked successfully"
                else:
                    raise Exception("You don't have permissions to perform this operation")
            else:
                raise Exception("Requested user is not related to the project")
            return BlockMemberMutation(status=status)
        raise Exception("You have to logged in to access api")

# add blog
class AddProjectBlogMutation(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        blog = BlogInputType()
    
    blog = graphene.Field(BlogType)

    @classmethod
    def mutate(cls, root, info, project_id, blog):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            author = User.objects.get(pk=user.id)
            if(author in project.members.all() or author in project.moderators.all() or author == project.admin):
                project_blog = Blog(author=author, title=blog.title, is_project_blog=True)
                if blog.data is not None:
                    project_blog.data = blog.data
                if blog.tags is not None:
                    project_blog.tags = blog.tags
                if blog.more_info is not None:
                    project_blog.more_info = blog.more_info
                
                project_blog.save()
                project.blogs.add(project_blog)
                project.save()
                return AddProjectBlogMutation(blog=project_blog)
            raise Exception("You don't have permissions to perform this action")
        raise Exception("You have to be logged in to access api")
    
class UpdateProjectBlogMutation(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        blog_id = graphene.ID(required=True)
        blog = BlogInputType()
    
    blog = graphene.Field(BlogType)

    @classmethod
    def mutate(cls, root, info, project_id, blog_id, blog):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            project_blog = Blog.objects.get(pk=blog_id)
            if(project_blog in project.blogs.all()):
                if(user.id == project_blog.author.id or user in project.moderators.all() or user.id == project.admin.id):
                    if blog.title is not None:
                        project_blog.title = blog.title
                    if blog.data is not None:
                        project_blog.data = blog.data
                    if blog.tags is not None:
                        project_blog.tags = blog.tags
                    if blog.more_info is not None:
                        project_blog.more_info = blog.more_info
                    project_blog.save()

                    return UpdateProjectBlogMutation(blog=project_blog)
                raise Exception("You don't have permissions to perform this action")
            raise Exception("Requested Blog is not found.")
        raise Exception("You have to be logged in to access api")

class DeleteProjectBlogMutation(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        blog_id = graphene.ID(required=True)
    
    status = graphene.String()
    
    @classmethod
    def mutate(cls, root, info, project_id, blog_id):
        user = info.context.user
        if(user.is_authenticated):
            project = Project.objects.get(pk=project_id)
            project_blog = Blog.objects.get(pk=blog_id)
            if(project_blog in project.blogs.all()):
                if(user.id == project_blog.author.id or user in project.moderators.all() or user.id == project.admin.id):
                    project_blog.delete()
                    return DeleteProjectBlogMutation(status="Blog deleted successfully")
                raise Exception("You don't have permissions to perform this action")
            raise Exception("Requested Blog is not found.")
        raise Exception("You have to be logged in to access api")