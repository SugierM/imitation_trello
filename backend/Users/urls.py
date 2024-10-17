from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.UserCreateView.as_view()),
    path('search_user/<str:first_name>/', views.UserSearchNameView.as_view()),
    path('user/', views.UserLoggedInView.as_view())
]