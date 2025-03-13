from rest_framework import serializers
from .models import Property
from organization.models import Organization
from district.models import District
from municipality.models import Municipality

class PropertySerializer(serializers.ModelSerializer):
    # You can add organization, district, and municipality as nested serializers or just reference the IDs
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all())

    class Meta:
        model = Property
        fields = ['id', 'district', 'municipality', 'name', 'street', 'created_by', 'created_date', 'last_modified_by', 'last_modified_date']
