from django.db import models
from .choices import AD_APPEAR_PLACES
class Country(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)

    # LOCAL (dev):
    image = models.ImageField(upload_to="countries/")

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

    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)

    # LOCAL(dev):
    image = models.ImageField(upload_to="cities/")
    appear_on_home_page = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name_en} ({self.country.name_en})"

class Slider(models.Model):
    # LOCAL(dev):
    image = models.ImageField(upload_to="sliders/")
    image_url = models.URLField(blank=True, null=True)
    appear_on_home_page = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Slider {self.id}"

class Ad(models.Model):
    # LOCAL(dev):
    image = models.ImageField(upload_to="ads/")

    image_url = models.URLField(blank=True, null=True)
    appear_place = models.CharField(
        max_length=20,
        choices=AD_APPEAR_PLACES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ad ({self.appear_place})"

class Feature(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)

    def __str__(self):
        return self.name_en

class Article(models.Model):
    title_en = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)

    # Markdown content
    content_en_md = models.TextField(
        help_text="Markdown content (English)"
    )
    content_ar_md = models.TextField(
        help_text="Markdown content (Arabic)"
    )

    meta = models.JSONField(blank=True, null=True)

    # LOCAL(dev):
    image = models.ImageField(upload_to="articles/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en
