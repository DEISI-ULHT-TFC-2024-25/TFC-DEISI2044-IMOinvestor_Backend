from django.db import models
from organization.models import Organization
from property.models import Property

class Announcement(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    


    class Meta:
        db_table = 'announcements'
