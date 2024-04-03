from django.db import models
from django.contrib.auth.models import AbstractUser


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
