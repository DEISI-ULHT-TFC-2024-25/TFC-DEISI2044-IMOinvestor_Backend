from rest_framework import serializers
from .models import PropertyMedia

class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = "__all__"

    def validate_file(self, value):
        if value.content_type.startswith('image'):
            if not value.name.lower().endswith(('jpg', 'jpeg', 'png')):
                raise serializers.ValidationError("Invalid image format. Use JPG or PNG.")
        elif value.content_type.startswith('video'):
            if not value.name.lower().endswith(('mp4', 'mov', 'avi')):
                raise serializers.ValidationError("Invalid video format. Use MP4, MOV or AVI.")
        else:
            raise serializers.ValidationError("Unsupported file type. Only images and videos are allowed.")
        return value
