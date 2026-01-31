from django.db import models
from django.conf import settings

from apps.core.validation import (
    validate_arabic_text,
    validate_english_text,
    validate_http_https_url,
    validate_image_is_image,
)


class Developer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="developer_profile"
    )

    name_en = models.CharField(max_length=255, validators=[validate_english_text])
    name_ar = models.CharField(max_length=255, validators=[validate_arabic_text])

    description_en = models.TextField(blank=False,null=False, validators=[validate_english_text])
    description_ar = models.TextField(blank=False ,null=False, validators=[validate_arabic_text])

    logo = models.ImageField(upload_to="developers/logos/", validators=[validate_image_is_image])
    website_url = models.CharField(max_length=500, blank=True, validators=[validate_http_https_url])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Developer"
        verbose_name_plural = "Developers"

    def __str__(self):
        return self.name_en
