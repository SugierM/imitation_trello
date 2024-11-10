# For now just .env
POSTGRES_USER=""
POSTGRES_PASSWORD=""

PGADMIN_DEFAULT_EMAIL=""  
PGADMIN_DEFAULT_PASSWORD=""

DJANGO_ALLOWED_HOSTS=""  
CORS_ALLOWED_ORIGINS=""  
DJANGO_DEBUG=""  
TIME_ZONE=""  
SECRET_KEY=""


VITE_API_URL=""  
HOST=""

### Overview to help myself :) 
Not a documentation for enduser.

# UI routes
"/" - Home (Protected route, accessible only to authenticated users.)  <br>
"/login" - Login form  <br>
"/logout" - Logout with redirection  <br>
"/register" - Register form  <br>
"/profile" - Profile page (Protected route, accessible only to authenticated users.) <br> 


# API routes
## Users
For all activieties must be authenticated.*  
`
"users/" - Main branch <br>
    ... create_user/ - User creation (login: email, password: passwords) <br>
        Doesn't have to be authenticated.  <br>

    ... search_user/ -  
        Takes one parameter in request - q  
        it can be first name, last name or nickname  

        {
            "count": int,
            "next": "",
            "previous": "",
            "results": [
                        "email": "email@email.com",
                        "nickname": "",
                        "first_name": "",
                        "last_name": "",
                        "url": ".../users/retr_user/int/"
            ]
        }

    ... profile/ - User profile information  
        Returns only information about logged in user.  

        *returns*
        {
            "email": "email@email.email",
            "first_name": "John",
            "last_name": "John",
            "bio": null,
            "phone": null,
            "nickname": "John",
            "last_login": null 
        }
        *last_login null for now as if you log in through frontend, it won't change  

    ... "profile_destroy/ - Deletes user profile (not tested)  

    ... "retr_user/<int:pk>/" - returns user and common boards with logged in user  

        Uses profile serializer so fields are generally the same
        {
            "email": "email@email.email",
            "first_name": "John",
            "last_name": "John",
            "bio": null,
            "phone": null,
            "nickname": "John",
            "last_login": null,
            "boards": [
            {
                "name": "Board name",
                "description": "Board description",
                "status": 0, # Ongoing or Done - here Ongoing
                "creator": {
                    "email": "email@email.com",
                    "nickname": "",
                    "first_name": "John",
                    "url": "[...]/users/retr_user/2/"
                }
            },
            ...
            ]
        }
`
*Exeptions signaled individually  

## Boards


`
boards/ - main branch  
Up to change as doesn't make sense in general

    ... boards_create/ - Creates board with specific details
        name - board name
        description - board description
        status - 0 or 1 where 0 means "Ongoing" and 1 means "Done"

    ... boards_destroy/int/ - Deletes board with specific ID

    ... boards/int/ - returns information about given board
        {
            "name": "Name",
            "description": "Description",
            "status": 0,
            "creator": {
                "email": "email@email.pl",
                "nickname": "",
                "first_name": "",
                "last_name": "",
                "url": ".../users/retr_user/int/"
            }
        }

    ... boards_list/ - returns list of boards user can see  
    {
        "count": int,
        "next": null,
        "previous": null,
        "results": [ 
            {
                "name": "Name",
                "status": 0,
                "board_url": ".../boards/boards/int/",
                "board_creator": "User Full Name"
            },
            ...
        ]
    }

    ... elements/int/ - returns information about specific element
        status - 0/1/2 > (Ongoing/Done/Postponed)
        order - defaults to 0
    {
        "board_url": ".../boards/boards/int/",
        "name": "Name",
        "description": "",
        "due_date": null,
        "order": 0,
        "status": 0
    }

    ... elements_create/ - Creates new task
        board - Board id
        name - Name
        description - Description
        due_date - Due date
        order - Order in which it shows on page
        status - 0/1/2 > (Ongoing/Done/Postponed)

        *Now due to some bugs you can't create elements without due_date  

    ... elements_destroy/int/ - Delets element with specific id

    ... elements_list/int/ - Returns list with elements that belong to board with specific id (from url)
        {
            "count": int,
            "next": null,
            "previous": null,
            "results": [
                {
                    "board_url": ".../boards/boards/3/",
                    "name": "Name",
                    "description": "Element task test see",
                    "due_date": null,
                    "order": 0,
                    "status": 0
                },
                ...
            ]
        }
`