from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """
    Менеджер пользователей для пользовательской модели User с использованием email вместо имени пользователя.
    Содержит методы для создания обычного пользователя и суперпользователя.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создаёт и сохраняет пользователя с указанным email и паролем.

        Аргументы:
            email (str): Email пользователя.
            password (str): Пароль пользователя.
            extra_fields (dict): Дополнительные поля для пользователя.

        Возвращает:
            User: Созданный объект пользователя.

        Исключения:
            ValueError: Если email не установлен.
        """

        if not email:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт обычного пользователя с указанным email и паролем.

        Аргументы:
            email (str): Email пользователя.
            password (str, optional): Пароль пользователя.
            extra_fields (dict): Дополнительные поля для пользователя. По умолчанию содержит is_staff=False
                                 и is_superuser=False.

        Возвращает:
            User: Созданный объект пользователя.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, tg_id, password=None, **extra_fields):
        """
        Создаёт суперпользователя с указанным email, идентификатором Телеграмма и паролем.

        Аргументы:
            email (str): Email суперпользователя.
            telegram_id (int): Идентификатор Телеграмма суперпользователя.
            password (str, optional): Пароль суперпользователя.
            extra_fields (dict): Дополнительные поля для пользователя. По умолчанию содержит is_staff=True
                                 и is_superuser=True.

        Возвращает:
            User: Созданный объект суперпользователя.

        Исключения:
            ValueError: Если is_staff или is_superuser не установлены в True.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        if not tg_id:
            raise ValueError("Необходимо указать идентификатор Телеграмма для суперпользователя.")

        extra_fields["tg_id"] = tg_id

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартную модель AbstractUser.

    Атрибуты:
        email : EmailField
            Поле для хранения электронной почты пользователя. Уникальное и обязательное.
        phone : CharField
            Поле для хранения номера телефона пользователя. Может быть пустым.
        city : CharField
            Поле для хранения города пользователя. Может быть пустым.
        avatar : ImageField
            Поле для хранения аватара пользователя. Может быть пустым.
        tg_id : BigIntegerField
            Поле для хранения ID пользователя в Telegram.

    Метапараметры:
        verbose_name : str
            Человекочитаемое имя модели в единственном числе.
        verbose_name_plural : str
            Человекочитаемое имя модели во множественном числе.

    Специальные атрибуты:
        USERNAME_FIELD : str
            Поле, используемое для входа пользователя (вместо стандартного username).
        REQUIRED_FIELDS : list
            Список обязательных полей (в дополнение к USERNAME_FIELD).

    Методы:
        __str__():
            Возвращает строковое представление объекта, равное электронной почте пользователя.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="телефон"
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="город")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="аватар"
    )
    tg_id = models.BigIntegerField(verbose_name="телеграм ID", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['tg_id']

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
