from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from role.models import Role  # Import Role model

class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, full_name="",  role=None):
        if not email:
            raise ValueError("Users must have an email address")
        

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number,
            role=role,  
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_organization(self, email, phone_number, password=None, full_name=""):
        org_role = Role.objects.get(name="Organization")  # Assign "Organization" role automatically
        return self.create_user(email, phone_number, password, full_name, role=org_role.id)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)  # One-to-Many Relationship

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role.name if self.role else 'No Role'})"
