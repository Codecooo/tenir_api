from django.db import models

class AlertLevel(models.TextChoices):
    SIAGA = 'siaga'
    WASPADA = 'waspada'
    AWAS = 'awas'

class DifficultyLevel(models.TextChoices):
    EASY = 'Gampang'
    MODERATE = 'Normal'
    CHALLENGING = 'Menantang'
    EXPERT = 'Expert'

# Create your models here.
class Mountain(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    height = models.DecimalField(max_digits=10, decimal_places=2)
    difficulty_level = models.CharField(
        max_length=50,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.EASY
    )
    region = models.CharField(max_length=100)
    indonesian_weekday_price = models.DecimalField(max_digits=10, decimal_places=2)
    indonesian_weekend_price = models.DecimalField(max_digits=10, decimal_places=2)
    international_weekday_price = models.DecimalField(max_digits=10, decimal_places=2)
    international_weekend_price = models.DecimalField(max_digits=10, decimal_places=2)
    alert_level = models.CharField(
        max_length=20,
        choices=AlertLevel.choices,
        default=AlertLevel.SIAGA
    )
    main_image = models.ImageField(upload_to='mountain_images/', max_length=255)
    is_favorite = models.BooleanField(default=False)
    is_volcanic_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'mountains'

class MountainPicture(models.Model):
    image = models.ImageField(upload_to='mountain_pictures/', max_length=255)
    description = models.TextField(blank=True, null=True)
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE, related_name='pictures')

    class Meta:
        db_table = 'mountain_pictures'