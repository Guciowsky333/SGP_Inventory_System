from django.db import models

# Create your models here.

class Localization(models.Model):
    localization_name = models.CharField(max_length=6)
    def __str__(self):
        return self.localization_name

class Component(models.Model):
    localization = models.ForeignKey(Localization, on_delete=models.CASCADE, related_name='components')
    code = models.CharField(max_length=6)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.code