from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    PLATFORM_CHOICES = [
        ('Trendyol', 'Trendyol'),
        ('Hepsiburada', 'Hepsiburada'),
        ('Amazon', 'Amazon'),
    ]
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=8, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20)
    store_url = models.URLField(blank=True, null=True)
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES, blank=True, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()