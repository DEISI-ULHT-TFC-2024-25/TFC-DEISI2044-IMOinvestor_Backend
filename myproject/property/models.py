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

    NOVA_CONSTRUCAO_CHOICES = [
        ('Sim', 'Sim'),
        ('Não', 'Não')
    ]

    CERTIFICADO_CHOICES = [
        ('F', 'F'),
        ('E', 'E'),
        ('D', 'D'),
        ('C', 'C'),
        ('B-', 'B-'),
        ('B', 'B'),
        ('A', 'A'),
        ('A+', 'A+')
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="properties")
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    street = models.CharField(max_length=510, blank=True, null=True)
    postal_code = models.CharField(max_length=10)
    property_type = models.CharField(max_length=255, choices=TIPO_CHOICE)
    imagens = models.JSONField(blank=True, null=True)  
    tipologia = models.CharField(max_length=50, blank=True, null=True)
    numero_casas_banho = models.CharField(max_length=10, blank=True, null=True)
    area_util = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    area_bruta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    preco_minimo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    preco_maximo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    nova_construcao = models.CharField(max_length=10, choices=NOVA_CONSTRUCAO_CHOICES, blank=True, null=True)
    certificado_energetico = models.CharField(max_length=10, choices=CERTIFICADO_CHOICES, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    informacoes_adicionais = models.JSONField(blank=True, null=True) 

    class Meta:
        db_table = 'property'

    def __str__(self):
        return self.name
