from rest_framework import serializers
from .models import Organization
from django.core.exceptions import ValidationError
from .models import validate_portuguese_nif  # ou de onde tiver colocado

class OrganizationSerializer(serializers.ModelSerializer):
    def validate_vat_number(self, value):
        validate_portuguese_nif(value)
        return value

    class Meta:
        model = Organization
        fields = "__all__"
