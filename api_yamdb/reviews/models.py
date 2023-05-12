from api.validators import validate_username
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

username_validator = UnicodeUsernameValidator()

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        'Никнейм',
        max_length=150,
        unique=True,
        validators=(username_validator, validate_username),
    )
    email = models.EmailField(
        'почта', max_length=254, unique=True, blank=False
    )
    first_name = models.CharField('Имя', max_length=150, blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)
    bio = models.TextField('О себе', blank=False)
    role = models.CharField(
        'Группа пользователей',
        max_length=255,
        choices=CHOICES,
        default=USER,
        blank=False,
        null=False,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='***',
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

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


class Title(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    text = models.TextField()
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Ревью'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.author
