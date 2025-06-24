from django.db import models
from django.conf import settings
from announcements.models import Announcement
from duser.models import DUser

class Investment(models.Model):
    user = models.ForeignKey(DUser, on_delete=models.CASCADE, related_name='investments')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='investments')
    invested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')
        db_table = 'investments'

    def __str__(self):
        return f"{self.user.user_name} invested in Announcement {self.announcement.id}"
