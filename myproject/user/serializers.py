from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_organization = serializers.BooleanField(default=False)  # NEW FIELD

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name','phone_number', 'is_organization']

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ""),
            phone_number=validated_data.get('phone_number', ""),
            is_organization=validated_data.get('is_organization', False)
        )
