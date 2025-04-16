from django.db import models
from district.models import District
from municipality.models import Municipality
from django.core.exceptions import ValidationError



def validate_portuguese_nif(value):
    if not value.isdigit() or len(value) != 9:
        raise ValidationError("O NIF deve conter exatamente 9 dígitos numéricos.")
    
    if int(value[0]) not in [1, 2, 3, 5, 6, 8, 9]:
        raise ValidationError("O NIF português deve começar com 1, 2, 3, 5, 6, 8 ou 9.")

    # Validação do dígito de controlo
    total = sum(int(d) * (9 - i) for i, d in enumerate(value[:8]))
    resto = total % 11
    digito_controlo = 0 if resto < 2 else 11 - resto

    if digito_controlo != int(value[8]):
        raise ValidationError("NIF inválido (dígito de controlo incorreto).")



class Organization(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    street = models.CharField(max_length=510)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    last_modified_by = models.CharField(max_length=255, null=True, blank=True)
    last_modified_date = models.DateTimeField(null=True, blank=True)
    vat_number = models.CharField(max_length=20, unique=True, validators=[validate_portuguese_nif])
    website = models.URLField(null=True, blank=True)




    class Meta:
        db_table = 'organization'

    def __str__(self):
        return self.name
