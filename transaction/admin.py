from django.contrib import admin

from transaction.models import Ticket, Transaction, Trip

# Register your models here.
admin.site.register([Transaction, Ticket, Trip])