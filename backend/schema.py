import graphene
from users.schema import AuthQuery, AuthMutation
from blogs.schema import BlogQuery, CreateBlogMutation, UpdateBlogMutation, DeleteBlogMutation 
from projects.schema import ( ProjectQuery, CreateProjectMutation, UpdateProjectMutation, DeleteProjectMutation,
    SendRequestMutation, AcceptRequestMutation, DeclineRequestMutation, MakeModeratorMutation,
    RemoveModeratorMutation, DeleteMemberMutation, BlockMemberMutation, UnBlockMemberMutation,
    AddProjectBlogMutation, UpdateProjectBlogMutation, DeleteProjectBlogMutation )

class Query(AuthQuery, BlogQuery, ProjectQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
    create_blog = CreateBlogMutation.Field()
    update_blog = UpdateBlogMutation.Field()
    delete_blog = DeleteBlogMutation.Field()

    create_project = CreateProjectMutation.Field()
    update_project = UpdateProjectMutation.Field()
    delete_project = DeleteProjectMutation.Field()

    send_request = SendRequestMutation.Field()
    accept_request = AcceptRequestMutation.Field()
    decline_request = DeclineRequestMutation.Field()

    make_moderator = MakeModeratorMutation.Field()
    remove_moderator = RemoveModeratorMutation.Field()
    delete_member = DeleteMemberMutation.Field()

    block_member = BlockMemberMutation.Field()
    unblock_member = UnBlockMemberMutation.Field()

    add_project_blog = AddProjectBlogMutation.Field()
    update_project_blog = UpdateProjectBlogMutation.Field()
    delete_project_blog = DeleteProjectBlogMutation.Field()
         
schema = graphene.Schema(query=Query, mutation=Mutation)
