from django.db import models
from organization.models import Organization
from phonenumber_field.modelfields import PhoneNumberField


class DUser(models.Model):

    LANG_KEY_CHOICES = [
        ('PT', 'Portuguese'),
        ('ENG', 'English')
    ]
    
    
    institution = models.ManyToManyField("organization.Organization", related_name="users")
    user_name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    lang_key = models.CharField(max_length=10, choices=LANG_KEY_CHOICES)
    activated = models.BooleanField()
    last_login = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USERNAME_FIELD = 'user_name'

    class Meta:
        db_table = 'd_user'

    def __str__(self):
        return self.user_name
    
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
