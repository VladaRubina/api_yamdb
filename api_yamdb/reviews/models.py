from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES = (
        (ADMIN, 'Admin'),
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        # ('S', 'Superuser'),
    )
    email = models.EmailField('почта', max_length=254, unique=True)
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Группа пользователей',
        max_length=255,
        choices=CHOICES,
        blank=True,
        default=USER,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX',
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(
        verbose_name='Идентификатор', max_length=50, unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
