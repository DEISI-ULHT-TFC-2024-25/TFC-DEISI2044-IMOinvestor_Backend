from django.db import models

class District(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'district'
