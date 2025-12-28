from django.db import models
from .choices import AD_APPEAR_PLACES
class Country(models.Model):
    name_en = models.CharField(max_length=255,unique=True) #validation english 
    name_ar = models.CharField(max_length=255,unique=True) #validation arabic
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

    name_en = models.CharField(max_length=255) #validation english 
    name_ar = models.CharField(max_length=255) #validation arabic

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
    image = models.ImageField(upload_to="sliders/") #required
    appear_on_home_page = models.BooleanField(default=True)
    index = models.IntegerField(default=0) #order of appearance and increasing
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Slider {self.id}"

class Ad(models.Model):
    image = models.ImageField(upload_to="ads/")
    appear_place = models.CharField(
        max_length=20,
        choices=AD_APPEAR_PLACES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ad ({self.appear_place})"

class Feature(models.Model):
    name_en = models.CharField(max_length=255) #validation english
    name_ar = models.CharField(max_length=255) #validation arabic

    def __str__(self):
        return self.name_en

class Article(models.Model):
    title_en = models.CharField(max_length=255) #validation english
    title_ar = models.CharField(max_length=255) #validation arabic

    # Markdown content
    content_en_md = models.TextField(
        help_text="Markdown content (English)"
    ) #validation english and markdown
    content_ar_md = models.TextField(
        help_text="Markdown content (Arabic)"
    ) #validation arabic and markdown

    meta = models.JSONField(blank=True, null=True)
    image = models.ImageField(upload_to="articles/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en
