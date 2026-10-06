from ninja import Schema
from typing import Optional

# ============================================
# REGISTER SCHEMA
# ============================================

class UserRegisterSchema(Schema):
    """Schema untuk user registration"""
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


# ============================================
# LOGIN SCHEMA
# ============================================

class UserLoginSchema(Schema):
    """Schema untuk user login"""
    email: str
    password: str


class TokenSchema(Schema):
    """Schema untuk token response"""
    access: str
    refresh: str


class LoginResponseSchema(Schema):
    """Schema untuk login response"""
    token: TokenSchema
    user: 'UserProfileSchema'


# ============================================
# USER PROFILE SCHEMA
# ============================================

class UserProfileSchema(Schema):
    """Schema untuk user profile"""
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    phone: str
    bio: str
    profile_picture: Optional[str] = None
    is_verified: bool
    is_active_hiker: bool
    created_at: str


class UserUpdateSchema(Schema):
    """Schema untuk update user profile"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None


# ============================================
# PASSWORD CHANGE SCHEMA
# ============================================

class ChangePasswordSchema(Schema):
    """Schema untuk change password"""
    old_password: str
    new_password: str
    confirm_password: str