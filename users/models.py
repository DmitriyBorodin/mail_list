from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")

    phone = models.CharField(
        max_length=35, blank=True, null=True, verbose_name="Телефон"
    )
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Город")
    avatar = models.ImageField(
        upload_to="users/avatars", blank=True, null=True, verbose_name="Аватарка"
    )
    token = models.CharField(max_length=100, verbose_name='токен', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ('set_active_user', 'Can activate user'),
            ('set_viewing_user', 'Can view user')
        ]

    def __str__(self):
        return self.email
