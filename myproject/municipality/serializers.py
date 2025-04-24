from rest_framework import serializers
from .models import Municipality

class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ['id', 'name', 'district']

class DistrictInputSerializer(serializers.Serializer):
    district_id = serializers.IntegerField()
