"""
Serializers for core models.
"""
from rest_framework import serializers
from .models import Country, City, Slider, Ad, Feature, Article


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            'id',
            'name_en',
            'name_ar',
            'image',
            'appear_on_home_page',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CitySerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name_en', read_only=True)
    
    class Meta:
        model = City
        fields = [
            'id',
            'country',
            'country_name',
            'name_en',
            'name_ar',
            'image',
            'appear_on_home_page',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = [
            'id',
            'image',
            'appear_on_home_page',
            'index',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = [
            'id',
            'image',
            'appear_place',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = [
            'id',
            'name_en',
            'name_ar'
        ]
        read_only_fields = ['id']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title_en',
            'title_ar',
            'content_en_md',
            'content_ar_md',
            'meta',
            'image',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
