from rest_framework import serializers
from django.contrib.auth import get_user_model
from role.models import Role  # Import Role model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role_id = serializers.IntegerField(write_only=True)  # Added role_id field

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'phone_number', 'role_id']  # Added role_id field

    def create(self, validated_data):
        role = Role.objects.get(id=validated_data['role_id'])  # Fetch the role by ID
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ""),
            phone_number=validated_data.get('phone_number', ""),
            role=role  # Assign the role
        )
