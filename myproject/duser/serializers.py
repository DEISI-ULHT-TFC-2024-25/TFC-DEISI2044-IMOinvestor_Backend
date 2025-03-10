from rest_framework import serializers
from .models import DUser
from user_roles.models import UserRole
from roles.models import Role
from user_organizations.models import UserOrganization
from organization.models import Organization
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

class DUserSerializer(serializers.ModelSerializer):
    institution_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = DUser
        fields = [
            'id', 'user_name', 'password_hash', 'first_name', 'last_name', 'email', 
            'date_of_birth', 'gender', 'lang_key', 'activated', 'last_login', 
            'created_by', 'created_date', 'last_modified_by', 'last_modified_date', 
            'institution_ids'
        ]

    def create(self, validated_data):
        institution_ids = validated_data.pop('institution_ids', [])
        
        # Hash password before storing it
        validated_data['password_hash'] = make_password(validated_data['password_hash'])
        
        # Set timestamps
        validated_data['created_date'] = now()
        
        user = DUser.objects.create(**validated_data)

        # Assign user to organizations
        for org_id in institution_ids:
            organization = Organization.objects.get(id=org_id)
            UserOrganization.objects.create(user=user, organization=organization, created_by=user.user_name, created_date=user.created_date)

        # Assign default "USER" role
        try:
            default_role = Role.objects.get(role="USER")  # Fetch the role with name "USER"
            UserRole.objects.create(user=user, role=default_role, created_by=user.user_name, created_date=now())
        except Role.DoesNotExist:
            raise serializers.ValidationError("Default role 'USER' does not exist in the database.")

        return user
