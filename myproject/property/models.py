from django.db import models
from district.models import District
from municipality.models import Municipality
from organization.models import Organization





class Property(models.Model):


    TIPO_CHOICE = [
        ('Apartamento', 'Apartamento'),
        ('Terreno', 'Terreno'),
        ('Casa', 'Casa'),
        ('Loja', 'Loja'),
        ('Armazém', 'Armazém'),
        ('Escritório', 'Escritório'),
        ('Quinta', 'Quinta'),
        ('Prédio', 'Prédio'),
        ('Garagem', 'Garagem'),
        ('Outro', 'Outro')
    ]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="properties")
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    street = models.CharField(max_length=510)
    created_by = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    property_type = models.CharField(max_length = 255,choices=TIPO_CHOICE)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'property'
