from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.UserCreateView.as_view()),
    path('search_user/<str:first_name>/', views.UserSearchNameView.as_view()),
    path('profile/', views.UserProfile.as_view(), name="user-profile"),
    path('retr_user/<int:pk>/', view=views.UserLookupView.as_view(), name="user-detail-lookup")
]