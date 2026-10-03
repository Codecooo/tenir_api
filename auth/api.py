# Mengimport fungsi autentikasi dari Django
from django.contrib.auth import authenticate, login, logout

# Mengimport model User bawaan Django
from django.contrib.auth.models import User

# Mengimport HttpResponse untuk response endpoint CSRF
from django.http import HttpResponse

# Mengimport decorator CSRF Django
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

# Mengimport Router dari Django Ninja
from ninja import Router

# Mengimport HttpError untuk membuat response error
from ninja.errors import HttpError

# Mengimport autentikasi berbasis session Django
# django_auth = user yang sudah login
# SessionAuthIsStaff = user yang login dan merupakan staff/admin
from ninja.security import django_auth, SessionAuthIsStaff

# Mengimport schema yang sudah dibuat
from .schema import RegisterIn, LoginIn, UserOut


# Membuat router untuk endpoint authentication
router = Router()


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

@router.post("/login", response=UserOut)
def login_user(request, payload: LoginIn):

    # Memeriksa username dan password
    user = authenticate(
        request,
        username=payload.username,
        password=payload.password
    )

    # Jika username atau password salah
    if user is None:
        raise HttpError(401, "Username atau password salah.")

    # Membuat session login
    login(request, user)

    # Mengembalikan data user
    return user


# =========================================================
# CURRENT USER / ME
# =========================================================

@router.get("/me", auth=django_auth, response=UserOut)
def current_user(request):

    # Mengambil user yang sedang login
    return request.auth


# =========================================================
# AUTHORIZATION / ADMIN ONLY
# =========================================================

@router.get("/admin-only", auth=SessionAuthIsStaff())
def admin_only(request):

    # Endpoint ini hanya dapat diakses
    # oleh user yang sudah login dan berstatus staff/admin
    return {
        "message": "Selamat datang di area admin.",
        "user": request.auth.username,
        "is_staff": request.auth.is_staff,
    }


# =========================================================
# CSRF TOKEN
# =========================================================

@router.get("/csrf", auth=None)
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):

    # Mengembalikan response kosong
    # Django akan membuat cookie csrftoken
    return HttpResponse()


# =========================================================
# LOGOUT
# =========================================================

@router.post("/logout", auth=django_auth)
def logout_user(request):

    # Menghapus session login user
    logout(request)

    # Mengembalikan pesan berhasil
    return {
        "message": "Logout berhasil."
    }