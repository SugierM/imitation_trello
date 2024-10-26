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
git
### Overview to help myself :) 
Not a documentation for enduser.

# UI routes
"/" - Home (Protected route, accessible only to authenticated users.)  
"/login" - Login form  
"/logout" - Logout with redirection  
"/register" - Register form  
"/profile" - Profile page (Protected route, accessible only to authenticated users.)  


# API routes
## Users
For all activieties must be authenticated.*  

"users/" - Main branch
    ... create_user/ - User creation (login: email, password: passwords)
        Doesn't have to be authenticated.  

    ... search_user/ - Search user based on first name  

    ... profile/ - User profile information  
        Returns only information about logged in user.  

        *returns*
        {
            "email": "email@email.email",
            "first_name": "John",
            "last_name": "John",
            "bio": null,
            "phone": null,
            "nickname": "John"
        }

    ... "retr_user/<int:pk>/" - returns user email and url to backend call
        Not working - non existent for url.
        {
            "email": "email@email.email",
            "url": ""
        }

*Exeptions signaled individually  

## Boards


"boards/"  

Routers were used. Implementation in progress.  