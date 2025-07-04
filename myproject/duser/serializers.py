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
from subscriptions.models import Subscription



class DUserSerializer(serializers.ModelSerializer):
    institution_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True
    )
    role_id = serializers.IntegerField(write_only=True)
    password = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = DUser
        fields = [
            'id', 'user_name', 'password', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'lang_key', 'activated', 'last_login', 
            'created_by', 'created_date', 'last_modified_by', 'last_modified_date', 
            'institution_ids', 'role_id'
        ]
        read_only_fields = ['created_date', 'last_login', 'created_by']

    def validate(self, data):
        role_id = data.get('role_id')
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            raise serializers.ValidationError({"role_id": "O papel fornecido não existe."})

        if role.role != "INVESTOR" and not data.get('institution_ids'):
            raise serializers.ValidationError({
                "institution_ids": "Este campo é obrigatório para papéis diferentes de INVESTOR."
            })

        data['role'] = role
        return data

    def create(self, validated_data):
        institution_ids = validated_data.pop('institution_ids', [])
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        validated_data.pop('role_id', None)  # <- aqui está a correção


        validated_data['password'] = make_password(password)
        validated_data['created_date'] = now()

        user = DUser.objects.create(**validated_data)

        # Associar papel fornecido
        UserRole.objects.create(
            user=user,
            role=role,
            created_by=user.user_name,
            created_date=now()
        )

        if role.role != "INVESTOR":
            for org_id in institution_ids:
                try:
                    organization = Organization.objects.get(id=org_id)
                    UserOrganization.objects.create(
                        user=user,
                        organization=organization,
                        created_by=user.user_name,
                        created_date=user.created_date
                    )
                except Organization.DoesNotExist:
                    raise serializers.ValidationError(f"Organização com ID {org_id} não existe.")

        return user
    





class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_name = data.get("user_name")
        password = data.get("password")

        expected_secret_key = settings.SECRET_KEY
        if expected_secret_key != "IMOINVESTOR2025":
            raise serializers.ValidationError("Internal secret key validation failed.")

        try:
            user = DUser.objects.get(user_name=user_name)
        except DUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid username or password")
        

        try:
            subscription = user.subscription
            if not subscription.is_valid():
                raise serializers.ValidationError("Subscription expired. Please renew.")
        except Subscription.DoesNotExist:
            raise serializers.ValidationError("No active subscription found. Please subscribe.")


        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)

        institution_ids = list(UserOrganization.objects.filter(user=user).values_list('organization_id', flat=True))
        roles = list(Role.objects.filter(userrole__user=user).values_list('role', flat=True))

        # Add custom user fields to token payload
        refresh['user_id'] = user.id
        refresh['user_name'] = user.user_name
        refresh['first_name'] = user.first_name
        refresh['last_name'] = user.last_name
        refresh['email'] = user.email
        refresh['phone'] = user.phone
        refresh['date_of_birth'] = user.date_of_birth.isoformat() if user.date_of_birth else None
        refresh['lang_key'] = user.lang_key
        refresh['activated'] = user.activated
        refresh['roles'] = roles
        refresh['organization_ids'] = institution_ids

        return {
            "user_id": user.id,
            "user_name": user.user_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "date_of_birth": user.date_of_birth,
            "lang_key": user.lang_key,
            "activated": user.activated,
            "organization_ids": institution_ids,
            "role": roles,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }



class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DUser
        fields = ['first_name', 'last_name', 'email', 'date_of_birth',  'lang_key']

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    



