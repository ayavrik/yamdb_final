from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    username = models.CharField(
        'Никнейм',
        db_index=True,
        max_length=255,
        unique=True
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        db_index=True,
        unique=True
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('Описание', max_length=500, blank=True)
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        default='user'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
