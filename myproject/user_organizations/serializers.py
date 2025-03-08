# user_organization/serializers.py
from rest_framework import serializers
from .models import UserOrganization

class UserOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrganization
        fields = ['user', 'organization', 'created_by', 'created_date']
