from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField 


class CreateUserDTO(serializers.Serializer):
    institution_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    user_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, max_length=255)
    first_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, allow_blank=True, required=False)
    date_of_birth = serializers.DateField(required=False)
    lang_key = serializers.ChoiceField(choices=[('PT', 'Portuguese'), ('ENG', 'English')])
    activated = serializers.BooleanField()
    created_by = serializers.CharField(max_length=255)
    role_id = serializers.IntegerField(write_only=True)  # New field added here

