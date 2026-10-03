from enum import Enum

from django.db import models

class AlertLevel(Enum):
    SIAGA = 'siaga'
    WASPADA = 'waspada'
    AWAS = 'awas'

class MountainPicture(models.Model):
    image = models.ImageField(upload_to='mountain_pictures/')
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'mountain_pictures'

# Create your models here.
class Mountain(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    height = models.DecimalField(max_digits=10, decimal_places=2)
    difficulty_level = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    indonesian_weekday_price = models.DecimalField(max_digits=10, decimal_places=2)
    indonesian_weekend_price = models.DecimalField(max_digits=10, decimal_places=2)
    international_weekday_price = models.DecimalField(max_digits=10, decimal_places=2)
    international_weekend_price = models.DecimalField(max_digits=10, decimal_places=2)
    alert_level = models.CharField(
        max_length=10,
        choices=[(level.value, level.name) for level in AlertLevel],
        default=AlertLevel.SIAGA.value
    )
    main_image = models.ImageField(upload_to='mountain_images/')
    pictures = models.ForeignKey(MountainPicture, on_delete=models.CASCADE) 
    is_favorite = models.BooleanField(default=False)
    is_volcanic_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'mountains'