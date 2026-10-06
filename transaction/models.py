from django.conf import settings
from django.db import models

from hiker.models import Hiker
from mountain.models import Mountain


class TransactionStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    CANCELLED = 'cancelled', 'Cancelled'
    FAILED = 'failed', 'Failed'
    EXPIRED = 'expired', 'Expired'


class Ticket(models.Model):
    hiker = models.ForeignKey(
        Hiker,
        on_delete=models.CASCADE
    )
    price_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = 'tickets'


class Trip(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    mountain = models.ForeignKey(
        Mountain,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('name', 'start_date', 'end_date', 'mountain')
        db_table = 'trips'


class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE
    )

    tickets = models.ManyToManyField(
        Ticket,
        related_name='transactions'
    )

    total_amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transactions'