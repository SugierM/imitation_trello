from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.UserCreateView.as_view()),
    path('search_user/', views.UserSearchView.as_view()),
    path('profile/', views.UserProfile.as_view()),
    path('retr_user/<int:pk>/', view=views.OtherUserPorfile.as_view(), name="user-detail-lookup"),
]