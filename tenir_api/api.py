from ninja import NinjaAPI

# Router JWT untuk mendapatkan access token
# dan refresh token
from ninja_jwt.routers.obtain import obtain_pair_router

from transaction.api import router as transaction_router
from hiker.api import router as hiker_router
from auth.api import router as auth_router


# Membuat instance utama Django Ninja API
api = NinjaAPI(title="Tenir API")


# =========================================================
# TRANSACTION
# =========================================================

api.add_router(
    "/transactions/",
    transaction_router,
    tags=["Transactions"]
)


# =========================================================
# HIKER
# =========================================================

api.add_router(
    "/hikers/",
    hiker_router,
    tags=["Hikers"]
)


# =========================================================
# AUTHENTICATION
# =========================================================

api.add_router(
    "/auth/",
    auth_router,
    tags=["Authentication"]
)


# =========================================================
# JWT TOKEN
# =========================================================

# Menambahkan router JWT bawaan django-ninja-jwt
# untuk obtain token dan refresh token
api.add_router(
    "/token/",
    obtain_pair_router,
    tags=["Authentication"]
)