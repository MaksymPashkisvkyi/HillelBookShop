from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле "Електронна адреса" є обовʼязковим.')
        if not phone:
            raise ValueError('Поле "Номер телефону" є обовʼязковим.')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, phone, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(unique=True, max_length=255)
    phone = models.CharField(_('Номер телефону'), max_length=13, unique=True)
    first_name = models.CharField(_('Імʼя'), max_length=30, blank=True)
    last_name = models.CharField(_('Прізвище'), max_length=50, blank=True)
    date_of_birth = models.DateField(_('Дата народження'), null=True, blank=True)
    profile_image = models.ImageField(_('Фото аватару'), upload_to='profile_avatars/', blank=True, null=True)
    is_staff = models.BooleanField(_('Статус персоналу'), default=False)
    is_active = models.BooleanField(_('Активований акаунт'), default=True)
    date_joined = models.DateTimeField(_('Дата реєстрації'), auto_now_add=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
