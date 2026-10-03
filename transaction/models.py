from django.conf import settings
from django.db import models

from mountain.models import Mountain


class TransactionStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    CANCELLED = 'cancelled', 'Cancelled'
    FAILED = 'failed', 'Failed'
    EXPIRED = 'expired', 'Expired'


class Hiker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    identity_number = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=15)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)


class Ticket(models.Model):
    hiker = models.ForeignKey(Hiker, on_delete=models.CASCADE)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)


class Trip(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE)


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    tickets: models.ManyToManyField[Ticket, Ticket] = models.ManyToManyField(
        Ticket, related_name='transactions'
    )
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)