from rest_framework import serializers
from .models import Investment

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'announcement', 'invested_at']
        read_only_fields = ['id', 'invested_at']
