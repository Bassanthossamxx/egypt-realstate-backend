from rest_framework import serializers

from .models import Developer


class DeveloperSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = getattr(self, 'context', {}).get('request')
        if request and isinstance(data.get('logo'), str) and data['logo'].startswith('/'):
            data['logo'] = request.build_absolute_uri(data['logo'])
        return data

    class Meta:
        model = Developer
        fields = [
            'id',
            'name_en',
            'name_ar',
            'description_en',
            'description_ar',
            'logo',
            'website_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
