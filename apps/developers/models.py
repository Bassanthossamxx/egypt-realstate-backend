from django.db import models
from django.conf import settings


class Developer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="developer_profile"
    )

    name_en = models.CharField(max_length=255) #validation english
    name_ar = models.CharField(max_length=255) #validation arabic

    description_en = models.TextField(blank=False,null=False) #validation english
    description_ar = models.TextField(blank=False ,null=False) #validation arabic

    logo = models.ImageField(upload_to="developers/logos/") #required
    website_url = models.URLField(blank=True) #validation url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Developer"
        verbose_name_plural = "Developers"

    def __str__(self):
        return self.name_en
