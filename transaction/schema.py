from typing import List
from ninja import ModelSchema, Schema
from .models import Ticket, Transaction, Trip
from hiker.schema import HikerOut

class TicketIn(ModelSchema):
    hiker_id: int
    class Meta:
        model = Ticket
        fields = ['price_paid']

class TicketOut(ModelSchema):
    hiker: HikerOut
    class Meta:
        model = Ticket
        fields = ['id', 'price_paid']


class TripIn(ModelSchema):
    mountain_id: int
    class Meta:
        model = Trip
        fields = ['name', 'start_date', 'end_date']

class TripOut(ModelSchema):
    mountain_id: int
    class Meta:
        model = Trip
        fields = ['id', 'name', 'start_date', 'end_date']

class TransactionIn(Schema):
    user_id: int
    trip_id: int
    total_amount_paid: float
    tickets: List[TicketIn]  
    status: str = 'pending'

class TransactionOut(ModelSchema):
    user_id: int
    trip_id: int
    tickets: List[TicketOut] 
    
    class Meta:
        model = Transaction
        fields = ['id', 'total_amount_paid', 'status', 'created_at']