# duser/serializers.py
from rest_framework import serializers
from .models import DUser
from user_organizations.models import UserOrganization
from organization.models import Organization

class DUserSerializer(serializers.ModelSerializer):
    # You can include a field for the organizations here (many-to-many relationship)
    institution_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = DUser
        fields = ['id', 'user_name', 'password_hash', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'lang_key', 'activated', 'last_login', 'created_by', 'created_date', 'last_modified_by', 'last_modified_date', 'institution_ids']

    def create(self, validated_data):
        institution_ids = validated_data.pop('institution_ids', [])
        user = DUser.objects.create(**validated_data)

        # Add user to the organizations (many-to-many relationship)
        for org_id in institution_ids:
            organization = Organization.objects.get(id=org_id)
            UserOrganization.objects.create(user=user, organization=organization, created_by=user.user_name, created_date=user.created_date)

        return user
