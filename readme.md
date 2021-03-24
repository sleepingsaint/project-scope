#Features

1. Implement User Management System
    - login
    - logout
    - register
    - verify user
    - check permission
    - generate jwt token
    - refresh jwt token
    - Implementing Email Backend
    - Describe the user model

2. Implementing models for projects
3. Implementing models for profile



# User model
    - bio
    - projects list
    - blogs list
    - avatar (implements at last)
    - badges for their accomplishments
        - most number of completed projects
        - maintaining active projects

## TODO
- Complete CRUD For Projects
- Complete CRUD For Badges
- implement user model
    - add the new fields as per above user model

### Learn
- Error Handling 
- Mutations

### Completed 

[x] basic CRUD For blogs

## Request Flow

- Request
    - send if he is not a member already or moderator or admin
    - send if he is not blocked
        - if blocked, send response request sent instead of blocked message


- Accept Request & Decline Request
    - accept only by admin or moderator
    - accept only if user exists in requests

- make moderator
    - made by admin
    - only if the user is already a member
    - if not member send a response that user needs to send request

- remove moderator
    - made by admin
    - only if user is moderator

- delete member
    - has to be a member or moderator

- block member / moderator
    - has to be admin for moderator or admin / moderator for member
    - user has to be member or 
    
- Unblock
    - remove user from unblocked list