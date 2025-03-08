from django.db import models
from property.models import Property

class PropertyRoi(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'property_roi'
