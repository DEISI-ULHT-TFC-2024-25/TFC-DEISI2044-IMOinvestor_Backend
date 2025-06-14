# announcements/serializers.py
from rest_framework import serializers
from .models import Announcement
from property.serializers import PropertySerializer  # Import here

class AnnouncementSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)  # Nest it

    class Meta:
        model = Announcement
        fields = "__all__"
