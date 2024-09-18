from typing import Any
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class CustomManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided valid email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email: str, password: str, **extra_fields: Any) -> Any:
        # if not email:
        #     raise ValueError('The Email must be set')
        # if not password:
        #     raise ValueError('The Password must be set')
        if not extra_fields.get('first_name'):
            raise ValueError('First name is required')
        
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> Any:
        # if not email:
        #     raise ValueError('The Email must be set')
        # if not password:
        #     raise ValueError('The Password must be set')
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=False, unique=True, null=False)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', null=False, default='avatars/avatar.png')
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=120, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']


    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email
    
    def get_short_name(self):
        if self.nickname:
            return self.nickname
        return self.email.split('@')[0]