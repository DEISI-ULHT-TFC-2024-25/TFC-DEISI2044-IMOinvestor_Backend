from django.db import models
from duser.models import DUser
from roles.models import Role

class UserRole(models.Model):
    user = models.ForeignKey(DUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_roles'
        unique_together = ['user', 'role']
