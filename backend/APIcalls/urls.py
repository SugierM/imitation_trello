from django.urls import path
from . import views
# from Users.models import User

urlpatterns = [
    path('test/', views.test),
    path('create_user/', views.UserCreateView.as_view()),
    path('view_user/<str:first_name>/', views.UserView.as_view()),
]