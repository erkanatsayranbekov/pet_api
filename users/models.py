from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        '''
        Creates and saves a User with the given email, date of
        birth and password.
        '''
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email).lower(),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    phone = models.CharField(max_length=12, validators=[RegexValidator(
        r'^\+7\d{1,10}$')], error_messages='Введите корректный номер телефона', )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email


class Teacher(models.Model):
    user = models.OneToOneField(
        UserAccount, related_name='teacher', on_delete=models.CASCADE)
    experience = models.TextField(verbose_name="Опыт", max_length=1000)
