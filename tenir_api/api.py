# tenir_api/api.py
from ninja import NinjaAPI
from transaction.api import router as transaction_router

api = NinjaAPI(title="Tenir API")

# Connect app routers
api.add_router("/transactions/", transaction_router, tags=["Transactions"])