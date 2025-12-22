from django.db import models


class AdAppearPlace(models.TextChoices):
    HOME = "home", "Home Page"
    PROJECTS = "projects", "Projects"
    UNITS = "units", "Units"
    OTHER = "other", "Other"

AD_APPEAR_PLACES = AdAppearPlace.choices
