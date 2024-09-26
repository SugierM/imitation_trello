from django.urls import path
from . import views
# from Users.models import User

urlpatterns = [
    path('test/', views.test),
]