from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле "Електронна адреса" є обовʼязковим.')
        if not phone_number:
            raise ValueError('Поле "Номер телефону" є обовʼязковим.')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, phone_number, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(unique=True, verbose_name='Електронна адреса', max_length=255)
    phone_number = models.CharField(max_length=10, unique=True, verbose_name='Номер телефону')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='Імʼя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Прізвище')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата народження')
    profile_image = models.ImageField(upload_to='profile_avatars/', blank=True, null=True, verbose_name='Фото аватару')
    is_staff = models.BooleanField(default=False, verbose_name='Статус персоналу')
    is_active = models.BooleanField(default=True, verbose_name='Активований акаунт')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата реєстрації')

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.email
