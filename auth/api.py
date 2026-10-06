# Mengimport fungsi authenticate dari Django
# Digunakan untuk mengecek username dan password
from django.contrib.auth import authenticate

# Mengimport model User bawaan Django
from django.contrib.auth.models import User

# Mengimport IntegrityError dan transaction
# Digunakan untuk menangani duplicate data dan race condition
from django.db import IntegrityError, transaction

# Mengimport Router dari Django Ninja
from ninja import Router

# Mengimport HttpError untuk membuat response error
from ninja.errors import HttpError

# Mengimport authentication JWT
from ninja_jwt.authentication import JWTAuth

# Mengimport token serializer untuk membuat
# access token dan refresh token
from ninja_jwt.tokens import RefreshToken

# Mengimport schema yang digunakan endpoint authentication
from .schema import RegisterIn, LoginIn, RegisterOut, UserOut


# Membuat router untuk endpoint authentication
router = Router()


# Membuat authentication JWT
# Endpoint yang menggunakan jwt_auth hanya dapat
# diakses jika request memiliki JWT yang valid
jwt_auth = JWTAuth()


# =========================================================
# REGISTER
# =========================================================

@router.post("/register", response={201: RegisterOut})
def register(request, payload: RegisterIn):

    # Mengecek apakah username atau email sudah digunakan
    if (
        User.objects.filter(username=payload.username).exists()
        or User.objects.filter(email=payload.email).exists()
    ):
        # Menggunakan pesan generic agar tidak membocorkan
        # apakah username atau email yang sudah terdaftar
        raise HttpError(
            400,
            "Username atau email sudah digunakan."
        )

    try:
        # Membuat transaksi database
        # agar proses pembuatan user berjalan secara aman
        with transaction.atomic():

            # Membuat user baru
            # create_user otomatis melakukan hashing password
            user = User.objects.create_user(
                username=payload.username,
                email=payload.email,
                password=payload.password,
                first_name=payload.first_name,
                last_name=payload.last_name,
            )

    # Menangani kemungkinan duplicate username/email
    # yang terjadi akibat request secara bersamaan
    except IntegrityError:
        raise HttpError(
            400,
            "Username atau email sudah digunakan."
        )

    # Register berhasil
    # Tidak mengembalikan object user
    return 201, {
        "message": "Registrasi berhasil."
    }


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login_user(request, payload: LoginIn):

    # Memeriksa username dan password menggunakan
    # sistem authentication bawaan Django
    user = authenticate(
        request,
        username=payload.username,
        password=payload.password
    )

    # Jika username atau password salah
    if user is None:
        raise HttpError(
            401,
            "Username atau password salah."
        )

    # Membuat refresh token berdasarkan user
    refresh = RefreshToken.for_user(user)

    # Mengembalikan access token,
    # refresh token, dan informasi user
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
        },
    }


# =========================================================
# CURRENT USER / ME
# =========================================================

@router.get("/me", auth=jwt_auth, response=UserOut)
def current_user(request):

    # Mengambil user berdasarkan JWT
    # yang dikirim melalui:
    # Authorization: Bearer <access_token>
    return request.auth


# =========================================================
# AUTHORIZATION / ADMIN ONLY
# =========================================================

@router.get("/admin-only", auth=jwt_auth)
def admin_only(request):

    # Mengambil user dari JWT
    user = request.auth

    # Mengecek apakah user merupakan staff/admin
    if not user.is_staff:
        raise HttpError(
            403,
            "Akses hanya untuk admin."
        )

    # Jika user adalah admin
    return {
        "message": "Selamat datang di area admin.",
        "user": user.username,
        "is_staff": user.is_staff,
    }