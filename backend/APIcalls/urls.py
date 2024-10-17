from django.urls import path, include
from . import views
# from Users.models import User
from Boards.views import BoardViewSet, TaskViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'board', BoardViewSet, basename='board')
router.register(r'task', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('test/', views.test)
    ]