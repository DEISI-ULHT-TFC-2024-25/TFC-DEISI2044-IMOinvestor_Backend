from rest_framework import serializers
from .models import DUser
from user_roles.models import UserRole
from roles.models import Role
from user_organizations.models import UserOrganization
from organization.models import Organization
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.utils import timezone 


from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken



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



class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_name = data.get("user_name")
        password = data.get("password")

        try:
            user = DUser.objects.get(user_name=user_name)
        except DUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        # Verifica a senha
        if not check_password(password, user.password_hash):
            raise serializers.ValidationError("Invalid username or password")
        
        user.last_login = timezone.now()
        user.save()

        # Gera tokens JWT
        refresh = RefreshToken.for_user(user)

        return {
            "user_id": user.id,
            "user_name": user.user_name,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
    


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DUser
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'lang_key']

    def update(self, instance, validated_data):
        # Use Django's default method to update the instance with validated data
        return super().update(instance, validated_data)

