from django.urls import path, include
from . import views
# from Users.models import User
from Boards.views import *

urlpatterns = [
    path('test/', views.test),
    path('boards_create/', view=BoardCreateView.as_view(), name='board-create'),
    path('boards_destroy/<int:pk>/', view=BoardDestroyView.as_view(), name='board-destroy'),
    path('boards/<int:pk>/', view=BoardView.as_view(), name='board-detail'),
    path('boards_list/', view=BoardListView.as_view(), name='board-list'),
    path('elements/<int:pk>/', view=ElementView.as_view(), name='element-detail'),
    path('elements_create/', view=ElementCreateView.as_view(), name='element-create'),
    path('elements_destroy/<int:pk>/', view=ElementDestroyView.as_view(), name='element-destroy'),
    path('elements_list/<int:board>/', view=ElementListView.as_view(), name='element-list')
    ]