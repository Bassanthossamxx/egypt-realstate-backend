"""
Serializers for core models.
"""
from django.db import transaction
from django.db.models import Max
from rest_framework import serializers
from .models import Country, City, Slider, Ad, Feature, Article


class AbsoluteMediaUrlMixin:
    media_fields: tuple[str, ...] = ()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = getattr(self, "context", {}).get("request")
        if not request:
            return data

        for field_name in self.media_fields:
            value = data.get(field_name)
            if isinstance(value, str) and value.startswith("/"):
                data[field_name] = request.build_absolute_uri(value)

        return data


class CountrySerializer(AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    media_fields = ("image",)

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


class CitySerializer(AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name_en', read_only=True)
    media_fields = ("image",)
    
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


class SliderSerializer(AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    media_fields = ("image",)

    def validate_index(self, value):
        if value is None:
            return value
        if int(value) < 0:
            raise serializers.ValidationError("index must be 0 or greater.")
        return value

    @staticmethod
    def _bump_sliders_with_conflicting_index(*, desired_index: int, exclude_id: int | None = None) -> None:
        conflict_qs = Slider.objects.select_for_update().filter(index=desired_index)
        if exclude_id is not None:
            conflict_qs = conflict_qs.exclude(id=exclude_id)

        conflicts = list(conflict_qs.order_by("id"))
        if not conflicts:
            return

        max_index = Slider.objects.select_for_update().aggregate(m=Max("index"))["m"]
        next_index = (max_index if max_index is not None else -1) + 1

        # If multiple conflicts exist (legacy duplicates), spread them at the end.
        for offset, slider in enumerate(conflicts):
            slider.index = next_index + offset
            slider.save(update_fields=["index"])

    def create(self, validated_data):
        desired_index = int(validated_data.get("index", 0) or 0)
        with transaction.atomic():
            self._bump_sliders_with_conflicting_index(desired_index=desired_index)
            return super().create(validated_data)

    def update(self, instance, validated_data):
        desired_index = validated_data.get("index", instance.index)
        desired_index = int(desired_index if desired_index is not None else 0)
        with transaction.atomic():
            if desired_index != instance.index:
                self._bump_sliders_with_conflicting_index(
                    desired_index=desired_index,
                    exclude_id=instance.id,
                )
            return super().update(instance, validated_data)

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


class AdSerializer(AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    media_fields = ("image",)

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


class ArticleSerializer(AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    media_fields = ("image",)

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
