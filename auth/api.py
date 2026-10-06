from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken

from .schema import LoginOut, RegisterIn, LoginIn, RegisterOut, UserOut


router = Router()

@router.post("/register", response={201: RegisterOut}, auth=None)
def register(request, payload: RegisterIn):
    # Membuat user sementara untuk menjalankan
    # validasi password Django
    user = User(
        username=payload.username,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )

    # Memvalidasi password menggunakan validator Django
    try:
        validate_password(payload.password, user=user)
    except ValidationError as exc:
        raise HttpError(
            400,
            "Password tidak memenuhi ketentuan: "
            + " ".join(exc.messages)
        )

    # Mengecek apakah username atau email sudah digunakan
    if (
        User.objects.filter(username=payload.username).exists()
        or User.objects.filter(email=payload.email).exists()
    ):
        raise HttpError(
            400,
            "Username atau email sudah digunakan."
        )

    # Membuat user secara aman di dalam database transaction
    try:
        with transaction.atomic():
            User.objects.create_user(
                username=payload.username,
                email=payload.email,
                password=payload.password,
                first_name=payload.first_name,
                last_name=payload.last_name,
            )
    except IntegrityError:
        # Menangani kemungkinan duplicate data
        # akibat race condition
        raise HttpError(
            400,
            "Username atau email sudah digunakan."
        )

    # Register berhasil
    return 201, {
        "message": "Registrasi berhasil."
    }

@router.post("/login", response=LoginOut, auth=None)
def login_user(request, payload: LoginIn):
    # Mengecek username dan password
    user = authenticate(
        request,
        username=payload.username,
        password=payload.password
    )

    # Jika login gagal
    if user is None:
        raise HttpError(
            401,
            "Username atau password salah."
        )

    # Membuat refresh token
    refresh = RefreshToken.for_user(user)

    # Mengembalikan access token, refresh token,
    # dan informasi user
    return LoginOut(
        access_token=str(refresh.access_token),
        refresh_token=str(refresh),
        user=UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_staff=user.is_staff,
        )
    )

@router.get("/me", response=UserOut)
def current_user(request):
    # Mengembalikan user yang sedang login
    return request.auth

@router.get("/admin-only")
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