from django.db import models
from district.models import District
from municipality.models import Municipality

class Organization(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    street = models.CharField(max_length=510)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)
    vat_number = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True,blank=True)

    
    class Meta:
        db_table = 'organization'

    def __str__(self):
        return self.name
