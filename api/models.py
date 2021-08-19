from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import my_year_validator


class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'
    USERS_ROLE = (
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Админ'),
    )
    email = models.EmailField('e-mail', unique=True)
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=10,
        choices=USERS_ROLE,
        default=ROLE_USER,
    )

    class Meta:
        ordering = ['id']

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Введи название категории',
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        help_text='Как твою категорию можно найти в поиске',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Введи название жанра',
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        help_text='Как твой жанр можно найти в поиске',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Введи название жанра',
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[my_year_validator],
        verbose_name="Год создания"
    )
    description = models.TextField(
        max_length=200,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Укажите категорию объекта',
    )


class Review(models.Model):
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    title = models.ForeignKey(
        Title,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
