from rest_framework import serializers

from .models import UnitType


class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = [
            'id',
            'name_en',
            'name_ar',
        ]
        read_only_fields = ['id']
