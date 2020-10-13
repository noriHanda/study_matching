from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from versatileimagefield.fields import VersatileImageField
from django.conf import settings
from django.core.validators import RegexValidator, EmailValidator


class UserManager(BaseUserManager):
    def create_user(
            self, username, email, password=None,
            **extra_fields):
        email = UserManager.normalize_email(email)
        user = self.model(
            username=username, email=email,
            **extra_fields)
        if password:
            user.set_password(password)
        user.is_rules_confirmed = True
        user.is_active = False
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if settings.DEBUG:
            user = self.create_user(username, email, password=password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.is_rules_confirmed = True
            user.save()
            return user
        else:
            raise RuntimeError("It is not valid function in production")


class User(PermissionsMixin, AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'username',
        max_length=20,
        unique=True,
        help_text=(
            '英数字と@, ., +, -, _が使えます'),
        validators=[username_validator],
        error_messages={
            'unique': "このユーザ名は既に登録されています",
        },
    )
    email = models.EmailField(
        'email',
        unique=True,
        help_text=(
              'hokudai.ac.jp で終わるメールアドレスのみ登録できます'),
        validators=[RegexValidator(regex=r'hokudai.ac.jp$', message='hokudai.ac.jp で終わるメールアドレスのみ登録できます'), EmailValidator]
    )
    intro = models.TextField('intro', max_length=200, blank=True)
    faculty = models.TextField('faculty', max_length=50, blank=True)
    department = models.TextField('department', max_length=50, blank=True)
    grade = models.TextField('grade', max_length=50, blank=True)
    hobby = models.TextField('hobby', max_length=200, blank=True)
    want_to_know = models.TextField('what want to know', max_length=400, blank=True)
    want_to_teach = models.TextField('what want to teach', max_length=400, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    is_active = models.BooleanField(default=False)
    icon = VersatileImageField('',upload_to='account', blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_rules_confirmed = models.BooleanField(default=False)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

