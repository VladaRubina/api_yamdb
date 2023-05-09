from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    CHOICES = (
        ('Ad', 'Admin'),
        ('An', 'Anonymous'),
        ('U', 'User'),
        ('M', 'Moderator'),
        ('S', 'Superuser'),
    )
    email = models.EmailField('Адрес почты', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=255, choices=CHOICES, blank=True)

    def __str__(self):
        return self.username
