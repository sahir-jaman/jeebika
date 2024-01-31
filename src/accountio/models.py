from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModelWithUID
from common.choices import UserType


# user manageer
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, confirm_password=None, type=None, phone=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            type=type,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser, BaseModelWithUID):
    email = models.EmailField(verbose_name="email address",max_length=255,unique=True)
    phone = PhoneNumberField(blank=True,null=True)
    type =  models.CharField(max_length=20, choices=UserType.choices, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # answer: All admins are staff
        return self.is_admin

