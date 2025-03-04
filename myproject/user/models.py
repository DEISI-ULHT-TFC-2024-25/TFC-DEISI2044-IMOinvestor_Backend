from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email,phone_number, password=None, full_name="", is_organization=False):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number,
            is_organization=is_organization
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_organization(self, email,phone_number, password=None, full_name=""):
        return self.create_user(email, password,phone_number, full_name, is_organization=True)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)  # NEW FIELD

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
