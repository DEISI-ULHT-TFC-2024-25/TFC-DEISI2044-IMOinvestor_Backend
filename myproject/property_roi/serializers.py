from rest_framework import serializers
from .models import ROICalculation

class ROICalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROICalculation
        fields = "__all__"
        read_only_fields = ['roi_result', 'profit']
