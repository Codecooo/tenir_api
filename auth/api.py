# Mengimport fungsi authenticate dari Django
# Digunakan untuk mengecek username dan password
from django.contrib.auth import authenticate

# Mengimport model User bawaan Django
from django.contrib.auth.models import User

# Mengimport Router dari Django Ninja
from ninja import Router

# Mengimport HttpError untuk membuat response error
from ninja.errors import HttpError

# Mengimport authentication JWT dari django-ninja-jwt
from ninja_jwt.authentication import JWTAuth

# Mengimport token serializer untuk membuat access dan refresh token
from ninja_jwt.tokens import RefreshToken

# Mengimport schema yang sudah dibuat
from .schema import RegisterIn, LoginIn, UserOut


# Membuat router untuk endpoint authentication
router = Router()


# Membuat authentication JWT
# Endpoint yang menggunakan jwt_auth
# hanya dapat diakses jika request memiliki JWT yang valid
jwt_auth = JWTAuth()


# =========================================================
# REGISTER
# =========================================================

@router.post("/register", response=UserOut)
def register(request, payload: RegisterIn):

    # Mengecek apakah username sudah digunakan
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username sudah digunakan.")

    # Mengecek apakah email sudah digunakan
    if User.objects.filter(email=payload.email).exists():
        raise HttpError(400, "Email sudah digunakan.")

    # Membuat user baru
    # create_user digunakan agar password otomatis di-hash
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )

    # Mengembalikan data user
    return user


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
        raise HttpError(401, "Username atau password salah.")

    # Membuat refresh token berdasarkan user
    refresh = RefreshToken.for_user(user)

    # Mengembalikan access token dan refresh token
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

    # Mengambil user berdasarkan JWT yang dikirim
    # melalui Authorization: Bearer <token>
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
        raise HttpError(403, "Akses hanya untuk admin.")

    # Jika user adalah admin
    return {
        "message": "Selamat datang di area admin.",
        "user": user.username,
        "is_staff": user.is_staff,
    }