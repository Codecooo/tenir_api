from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model dengan field tambahan untuk aplikasi Tenir
    """
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        help_text="Nomor telepon user"
    )
    
    # Profile info
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        blank=True, 
        null=True,
        help_text="Foto profil user"
    )
    bio = models.TextField(
        blank=True, 
        help_text="Biografi singkat"
    )
    
    # Status
    is_verified = models.BooleanField(
        default=False,
        help_text="Email sudah diverifikasi"
    )
    is_active_hiker = models.BooleanField(
        default=False,
        help_text="Apakah user adalah hiker yang aktif"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Override groups dan user_permissions dengan related_name yang unik
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_groups'  # ← TAMBAH related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permissions'  # ← TAMBAH related_name
    )
    
    # Set email sebagai USERNAME_FIELD untuk login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"
    
    def get_full_name(self):
        """Return nama lengkap user"""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()