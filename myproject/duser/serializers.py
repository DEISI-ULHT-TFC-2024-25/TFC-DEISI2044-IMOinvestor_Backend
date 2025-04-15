from rest_framework import serializers
from .models import DUser
from user_roles.models import UserRole
from roles.models import Role
from user_organizations.models import UserOrganization
from organization.models import Organization
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.utils import timezone 
from django.conf import settings
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken



from .dtos import CreateUserDTO

class DUserSerializer(serializers.ModelSerializer):
    institution_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    password = serializers.CharField(write_only=True, max_length=255)  # Replace password_hash

    class Meta:
        model = DUser
        fields = [
            'id', 'user_name', 'password', 'first_name', 'last_name', 'email', 
            'date_of_birth', 'lang_key', 'activated', 'last_login', 
            'created_by', 'created_date', 'last_modified_by', 'last_modified_date', 
            'institution_ids'
        ]
        read_only_fields = ['created_date', 'last_login', 'created_by']

    def create(self, validated_data):
        institution_ids = validated_data.pop('institution_ids', [])
        password = validated_data.pop('password')

        validated_data['password_hash'] = make_password(password)
        validated_data['created_date'] = now()

        user = DUser.objects.create(**validated_data)

        for org_id in institution_ids:
            organization = Organization.objects.get(id=org_id)
            UserOrganization.objects.create(user=user, organization=organization, created_by=user.user_name, created_date=user.created_date)

        try:
            default_role = Role.objects.get(role="USER")
            UserRole.objects.create(user=user, role=default_role, created_by=user.user_name, created_date=now())
        except Role.DoesNotExist:
            raise serializers.ValidationError("Default role 'USER' does not exist.")

        return user




class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_name = data.get("user_name")
        password = data.get("password")

        # Secret key is internal – not provided by user
        expected_secret_key = settings.SECRET_KEY

        if expected_secret_key != "IMOINVESTOR2025":
            raise serializers.ValidationError("Internal secret key validation failed.")

        try:
            user = DUser.objects.get(user_name=user_name)
        except DUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if not check_password(password, user.password_hash):
            raise serializers.ValidationError("Invalid username or password")
        
        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)

        institution_ids = list(user.institution.values_list('id', flat=True))
        roles = Role.objects.filter(userrole__user=user).values_list('role', flat=True)

        
        refresh.payload['roles'] = list(roles)
        refresh.payload['organization_ids'] = institution_ids


        print(f"Signing Secret Key: {settings.SECRET_KEY}")


        return {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization_ids": institution_ids,
            "role": roles,
            "user_name": user.user_name,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }




class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DUser
        fields = ['first_name', 'last_name', 'email', 'date_of_birth',  'lang_key']

    def update(self, instance, validated_data):
        # Use Django's default method to update the instance with validated data
        return super().update(instance, validated_data)

