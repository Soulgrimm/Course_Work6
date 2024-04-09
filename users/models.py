from django.contrib.auth.models import AbstractUser
from django.db import models
import random

from main.models import NULLABLE

code = ''.join([str(random.randint(0, 9)) for _ in range(6)])


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=40, verbose_name='Страна')
    is_active = models.BooleanField(default=False, verbose_name='Активность')

    confirm_code = models.CharField(default=code, max_length=6, verbose_name='Код')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
