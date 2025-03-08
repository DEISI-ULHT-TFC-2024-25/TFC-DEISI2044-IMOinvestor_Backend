from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [
        ('SYS_ADMIN', 'System Administrator'),
        ('USER', 'User')
    ]
    
    role = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.role
