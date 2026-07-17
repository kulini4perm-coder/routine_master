from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """ Кастомный менеджер для модели пользователя,
        где email - уникальный идентификатор вместо username """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email должно быть заполнено')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите адрес электронной почты"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите изображение профиля",
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город проживания",
    )
    tg_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Telegram Chat ID",
        help_text="Идентификатор чата в Telegram для отправки уведомлений",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email



