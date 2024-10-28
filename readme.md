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

*Exeptions signaled individually  

## Boards


"boards/"  

Routers were used. Implementation in progress.  