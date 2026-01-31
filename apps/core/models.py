from django.db import models
from .choices import AD_APPEAR_PLACES
from .validation import (
    validate_arabic_text,
    validate_english_text,
    validate_image_webp_only,
    validate_image_is_image,
    validate_image_is_webp,
    validate_markdown_text,
)

class Country(models.Model):
    name_en = models.CharField(max_length=255,unique=True, validators=[validate_english_text])
    name_ar = models.CharField(max_length=255,unique=True, validators=[validate_arabic_text])
    image = models.ImageField(upload_to="countries/", validators=[validate_image_webp_only, validate_image_is_webp])

    appear_on_home_page = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name_en

class City(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities"
    )

    name_en = models.CharField(max_length=255, validators=[validate_english_text])
    name_ar = models.CharField(max_length=255, validators=[validate_arabic_text])
    image = models.ImageField(upload_to="cities/", validators=[validate_image_webp_only, validate_image_is_webp])
    appear_on_home_page = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name_en} ({self.country.name_en})"

class Slider(models.Model):
    image = models.ImageField(upload_to="sliders/", validators=[validate_image_is_image])
    appear_on_home_page = models.BooleanField(default=True)
    index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["index", "id"]

    def __str__(self):
        return f"Slider {self.id}"

class Ad(models.Model):
    image = models.ImageField(upload_to="ads/", validators=[validate_image_webp_only, validate_image_is_webp])
    appear_place = models.CharField(
        max_length=20,
        choices=AD_APPEAR_PLACES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ad ({self.appear_place})"

class Feature(models.Model):
    name_en = models.CharField(max_length=255, validators=[validate_english_text])
    name_ar = models.CharField(max_length=255, validators=[validate_arabic_text])

    def __str__(self):
        return self.name_en

class Article(models.Model):
    title_en = models.CharField(max_length=255, validators=[validate_english_text]) 
    title_ar = models.CharField(max_length=255, validators=[validate_arabic_text])

    # Markdown content
    content_en_md = models.TextField(
        help_text="Markdown content (English)"
    ,
        validators=[validate_markdown_text, validate_english_text],
    ) #validation english and markdown
    content_ar_md = models.TextField(
        help_text="Markdown content (Arabic)"
    ,
        validators=[validate_markdown_text, validate_arabic_text],
    ) #validation arabic and markdown

    meta = models.JSONField(blank=True, null=True)
    image = models.ImageField(upload_to="articles/", validators=[validate_image_webp_only, validate_image_is_webp])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en


class StoredMedia(models.Model):
    """Database-backed storage for uploaded media files."""

    name = models.CharField(max_length=500, unique=True)
    original_name = models.CharField(max_length=500, blank=True)
    content_type = models.CharField(max_length=200, blank=True)
    size = models.PositiveIntegerField(default=0)
    data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Stored Media"
        verbose_name_plural = "Stored Media"

    def __str__(self):
        return self.name
