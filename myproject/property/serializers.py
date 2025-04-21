from rest_framework import serializers
from .models import Property
from organization.models import*  

class PropertySerializer(serializers.ModelSerializer):
    
    organization_id = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), source='organization', write_only=True)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all())
    area_util = serializers.FloatField(required=False)
    area_bruta = serializers.FloatField(required=False)
    preco_minimo = serializers.FloatField(required=False)
    preco_maximo = serializers.FloatField(required=False)
    informacoes_adicionais = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False
    )

    class Meta:
        model = Property
        fields = [
            'id',
            'organization_id',  
            'district',
            'municipality',
            'name',
            'street',
            'postal_code',
            'property_type',
            'imagens',
            'tipologia',
            'numero_casas_banho',
            'area_util',
            'area_bruta',
            'preco_minimo',
            'preco_maximo',
            'nova_construcao',
            'certificado_energetico',
            'descricao',
            'informacoes_adicionais',
        ]
