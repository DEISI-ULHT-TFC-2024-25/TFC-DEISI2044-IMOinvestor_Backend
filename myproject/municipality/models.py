from django.db import models
from district.models import District

class Municipality(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'municipality'
        unique_together = ['name', 'district']

    def __str__(self):
        return self.name
