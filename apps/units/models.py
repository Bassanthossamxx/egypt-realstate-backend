from django.db import models

from apps.core.validation import validate_arabic_text, validate_english_text

class UnitType(models.Model):
    name_en = models.CharField(max_length=100, unique=True, validators=[validate_english_text])
    name_ar = models.CharField(max_length=100, unique=True, validators=[validate_arabic_text])

    def __str__(self):
        return self.name_en
