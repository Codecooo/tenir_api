from ninja import Router
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from user.serializers import (
    UserRegisterSchema,
    UserLoginSchema,
    TokenSchema,
    LoginResponseSchema,
    UserProfileSchema,
    UserUpdateSchema,
    ChangePasswordSchema
)

router = Router()


# ============================================
# AUTHENTICATION ENDPOINTS
# ============================================

@router.post("/auth/register", response=UserProfileSchema, tags=["Authentication"])
def register(request, payload: UserRegisterSchema):
    """
    Register user baru
    Required:
    - username
    - email
    - password
    - first_name (optional)
    - last_name (optional)
    - phone (optional)
    """
    
    # Check if user already exists
    if User.objects.filter(email=payload.email).exists():
        return {"error": "Email sudah terdaftar"}, 400
    
    if User.objects.filter(username=payload.username).exists():
        return {"error": "Username sudah terdaftar"}, 400
    
    # Create user
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name or "",
        last_name=payload.last_name or "",
        phone=payload.phone or ""
    )
    
    return user


@router.post("/auth/login", response=LoginResponseSchema, tags=["Authentication"])
def login(request, payload: UserLoginSchema):
    """
    Login user
    Required:
    - email
    - password
    
    Returns: token (access & refresh) + user profile
    """
    
    # Get user by email
    try:
        user = User.objects.get(email=payload.email)
    except User.DoesNotExist:
        return {"error": "Email atau password salah"}, 401
    
    # Authenticate password
    user = authenticate(username=user.username, password=payload.password)
    
    if user is None:
        return {"error": "Email atau password salah"}, 401
    
    # Generate token
    refresh = RefreshToken.for_user(user)
    
    return {
        "token": {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        },
        "user": user
    }


@router.post("/auth/refresh", response=TokenSchema, tags=["Authentication"])
def refresh_token(request, refresh: str):
    """
    Refresh access token menggunakan refresh token
    """
    try:
        refresh_token = RefreshToken(refresh)
        return {
            "access": str(refresh_token.access_token),
            "refresh": str(refresh_token)
        }
    except Exception as e:
        return {"error": f"Invalid refresh token: {str(e)}"}, 401


# ============================================
# USER PROFILE ENDPOINTS
# ============================================

@router.get("/users/me", response=UserProfileSchema, tags=["User"])
def get_current_user(request):
    """
    Get profile user yang sedang login
    Require: Authorization header dengan token
    """
    if not request.user.is_authenticated:
        return {"error": "Unauthorized"}, 401
    
    return request.user


@router.get("/users/{user_id}", response=UserProfileSchema, tags=["User"])
def get_user_profile(request, user_id: int):
    """
    Get public profile user by ID
    """
    user = get_object_or_404(User, id=user_id)
    return user


@router.get("/users", response=list[UserProfileSchema], tags=["User"])
def list_users(request):
    """
    List semua users (public profiles)
    """
    return User.objects.all()


# ============================================
# UPDATE ENDPOINTS
# ============================================

@router.put("/users/me", response=UserProfileSchema, tags=["User"])
def update_profile(request, payload: UserUpdateSchema):
    """
    Update profile user yang sedang login
    Require: Authorization header dengan token
    """
    if not request.user.is_authenticated:
        return {"error": "Unauthorized"}, 401
    
    user = request.user
    
    # Update hanya field yang dikirim
    if payload.first_name:
        user.first_name = payload.first_name
    if payload.last_name:
        user.last_name = payload.last_name
    if payload.phone:
        user.phone = payload.phone
    if payload.bio:
        user.bio = payload.bio
    if payload.profile_picture:
        user.profile_picture = payload.profile_picture
    
    user.save()
    return user


@router.post("/users/change-password", tags=["User"])
def change_password(request, payload: ChangePasswordSchema):
    """
    Change password user yang sedang login
    Require: Authorization header dengan token
    """
    if not request.user.is_authenticated:
        return {"error": "Unauthorized"}, 401
    
    user = request.user
    
    # Verify old password
    if not user.check_password(payload.old_password):
        return {"error": "Password lama salah"}, 400
    
    # Check if new password matches confirm password
    if payload.new_password != payload.confirm_password:
        return {"error": "Password baru tidak cocok"}, 400
    
    # Check if new password same with old password
    if payload.old_password == payload.new_password:
        return {"error": "Password baru tidak boleh sama dengan password lama"}, 400
    
    # Set new password
    user.set_password(payload.new_password)
    user.save()
    
    return {"message": "Password berhasil diubah"}


# ============================================
# DELETE ENDPOINT
# ============================================

@router.delete("/users/me", tags=["User"])
def delete_account(request):
    """
    Delete account user yang sedang login
    Require: Authorization header dengan token
    """
    if not request.user.is_authenticated:
        return {"error": "Unauthorized"}, 401
    
    user = request.user
    username = user.username
    user.delete()
    
    return {"message": f"Account '{username}' berhasil dihapus"}