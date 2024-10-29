from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', view=views.UserCreateView.as_view(), name='user-create'),
    path('search_user/', view=views.UserSearchView.as_view(), name='user-search'),
    path('profile/', view=views.UserProfileView.as_view(), name='user-profile'),
    path('profile_destroy/', view=views.UserProfileDeleteView.as_view(), name='user-delete'),
    path('retr_user/<int:pk>/', view=views.OtherUserPorfileView.as_view(), name="user-detail-lookup"),
]