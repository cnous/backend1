from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    custom user model manager where email is the unique identifiication for authentication instead of usernames
    """

    def create_user(self,email, password, **extra_fields):
        """
        create and save a user with the given email and password
        """
        if not email:
            raise ValueError(_("the email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        create and save superuser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('superuser must have is_staff True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('superuser must have is_superuser True'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom user model for our app
    """
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)

    objects = UserManager()

    def __str__(self):
        return self.email