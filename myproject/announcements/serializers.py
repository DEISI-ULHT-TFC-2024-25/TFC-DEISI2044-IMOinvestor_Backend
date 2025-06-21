# announcements/serializers.py
from rest_framework import serializers
from .models import Announcement
from property.serializers import PropertySerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    property = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = "__all__"

    def get_property(self, obj):
        request = self.context.get('request')
        method = request.method if request else None

        # Show full property details only on GET requests
        if method in ['GET']:
            return PropertySerializer(obj.property, context=self.context).data
        else:
            return obj.property.id
