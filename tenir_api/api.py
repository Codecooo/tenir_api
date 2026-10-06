from ninja import NinjaAPI
from transaction.api import router as transaction_router
from hiker.api import router as hiker_router
from mountain.api import router as mountain_router
from user.api import router as user_router
from equipment.api import router as equipment_router

api = NinjaAPI(title="Tenir API")

# Connect app routers
api.add_router("/transactions/", transaction_router, tags=["Transactions"])
api.add_router("/hikers/", hiker_router, tags=["Hikers"])
api.add_router("/", mountain_router)
api.add_router("/", user_router)
api.add_router("/", equipment_router)