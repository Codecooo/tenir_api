from ninja import NinjaAPI

# Router JWT untuk mendapatkan access token
# dan refresh token
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.routers.obtain import obtain_pair_router

from transaction.api import router as transaction_router
from hiker.api import router as hiker_router
from auth.api import router as auth_router


auth = JWTAuth()
api = NinjaAPI(title="Tenir API", version="1.0", auth=auth)

api.add_router(
    "/transactions/",
    transaction_router,
    tags=["Transactions"]
)

api.add_router(
    "/hikers/",
    hiker_router,
    tags=["Hikers"]
)

api.add_router(
    "/auth/",
    auth_router,
    tags=["Authentication"]
)

api.add_router(
    "/token/",
    obtain_pair_router,
    tags=["Authentication"]
)