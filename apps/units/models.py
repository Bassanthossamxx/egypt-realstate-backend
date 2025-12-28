from django.db import models

class UnitType(models.Model):
    name_en = models.CharField(max_length=100) #validation english
    name_ar = models.CharField(max_length=100) #validation arabic

    def __str__(self):
        return self.name_en
