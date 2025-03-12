from django.db import models
from district.models import District
from municipality.models import Municipality
from organization.models import Organization

class Property(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    street = models.CharField(max_length=510)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'property'
