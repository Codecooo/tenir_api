from ninja import NinjaAPI
from transaction.api import router as transaction_router
from hiker.api import router as hiker_router

api = NinjaAPI(title="Tenir API")

# Connect app routers
api.add_router("/transactions/", transaction_router, tags=["Transactions"])
api.add_router("/hikers/", hiker_router, tags=["Hikers"])