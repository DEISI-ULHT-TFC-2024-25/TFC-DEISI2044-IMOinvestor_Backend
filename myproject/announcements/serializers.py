from rest_framework import serializers
from property.models import Property
from .models import Announcement
from property.serializers import PropertySerializer


class AnnouncementSerializer(serializers.ModelSerializer):
    # For GET responses: nested property object (read-only)
    property = PropertySerializer(read_only=True)

    # For POST/PUT input: write-only property_id field
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(),
        write_only=True,
        source='property'
    )

    is_favourite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'property', 'property_id', 'price', 'created_date', 'created_by',
            'last_modified_date', 'last_modified_by', 'expiry_date', 'is_active', 'is_favourite'
        ]
        read_only_fields = ['property', 'is_favourite']

    def get_is_favourite(self, obj):
        # Example implementation, adjust as needed
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj in user.favourites.all()
        return False


class AnnouncementInputSerializer(serializers.ModelSerializer):
    # Input serializer for POST/PUT, only property_id (no nested property)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(),
        source='property'
    )

    class Meta:

        model = Announcement
        fields = [
            'property_id', 'price', 'created_date', 'created_by',
            'last_modified_date', 'last_modified_by', 'expiry_date', 'is_active'
        ]
class AnnouncementIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id']
class AnnouncementIdInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class AnnouncementUpdateSerializer(serializers.ModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(),
        source='property'

    )

    class Meta:
        model = Announcement
        fields = ['property_id', 'price','is_active']
