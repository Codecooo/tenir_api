from django.db import models

class Hiker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    identity_number = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=15)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'hikers'
