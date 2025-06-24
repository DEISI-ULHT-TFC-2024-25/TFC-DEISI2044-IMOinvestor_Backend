from django.db import models
from django.utils import timezone
from datetime import timedelta
from duser.models import DUser  # adjust the import if your user model is custom

class Subscription(models.Model):
    user = models.OneToOneField(DUser, on_delete=models.CASCADE, related_name='subscription')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()
