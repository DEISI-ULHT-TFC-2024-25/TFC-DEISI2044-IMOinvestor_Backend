from django.db import models
from property.models import Property

class PropertyMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video')
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="property_media/",null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'property_media'

    def __str__(self):
        return f"{self.property.id} - {self.media_type}"
