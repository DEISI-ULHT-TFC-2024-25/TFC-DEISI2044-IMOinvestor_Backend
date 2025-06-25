from rest_framework import serializers
from .models import Property
from organization.models import*  



class PropertySerializer(serializers.ModelSerializer):
    ##organization_id = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), source='organization', write_only=True)
    organization_id = serializers.IntegerField(source='organization.id', read_only=True)

    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    district_name = serializers.SerializerMethodField(read_only=True)

    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all())
    municipality_name = serializers.SerializerMethodField(read_only=True)


    property_type = serializers.ChoiceField(choices=Property.TIPO_CHOICE)
    new_construction = serializers.ChoiceField(choices=Property.NOVA_CONSTRUCAO_CHOICES, required=False, allow_null=True)
    energy_certf = serializers.ChoiceField(choices=Property.CERTIFICADO_CHOICES, required=False, allow_null=True)

    net_area = serializers.FloatField(required=False)
    gross_area = serializers.FloatField(required=False)
    min_price = serializers.FloatField(required=False)
    max_price = serializers.FloatField(required=False)

    informacoes_adicionais = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False
    )


    def get_district_name(self, obj):
        return obj.district.name if obj.district else None

    def get_municipality_name(self, obj):
        return obj.municipality.name if obj.municipality else None

    class Meta:
        model = Property
        fields = [
            'id',
            'district',
            'district_name',        
            'municipality',
            'municipality_name',
            'name',
            'street',
            'postal_code',
            'property_type', 
            'imagens',
            'typology',
            'num_wc',
            'net_area',
            'gross_area',
            'min_price',
            'max_price',
            'new_construction',  # now explicitly defined
            'energy_certf',  # now explicitly defined
            'description',
            'informacoes_adicionais',
            'organization_id',
        ]
