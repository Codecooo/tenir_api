from typing import List
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Ticket, Transaction
from .schema import TransactionIn, TransactionOut

router = Router()

@router.post("/new", response=TransactionOut)
def create_transaction(payload: TransactionIn):
    with transaction.atomic():
        # Create the parent Transaction instance
        trx = Transaction.objects.create(
            user_id=payload.user_id,
            trip_id=payload.trip_id,
            total_amount_paid=payload.total_amount_paid,
            status=payload.status,
        )

        # Instantiate and bulk-create child Tickets
        ticket_instances = [
            Ticket(
                hiker_id=ticket_data.hiker_id,
                price_paid=ticket_data.price_paid
            )
            for ticket_data in payload.tickets
        ]
        created_tickets = Ticket.objects.bulk_create(ticket_instances)

        # Associate created tickets with the ManyToMany field
        trx.tickets.set(created_tickets)

    return trx


@router.get("/{transaction_id}", response=TransactionOut)
def get_transaction(transaction_id: int):
    trx = get_object_or_404(
        Transaction.objects.prefetch_related('tickets__hiker'),
        id=transaction_id
    )
    return trx


@router.get("/user/<int:user_id>", response=List[TransactionOut])
def list_user_transactions(user_id: int):
    return Transaction.objects.prefetch_related('tickets__hiker').filter(user_id=user_id)