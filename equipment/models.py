from django.db import models

class Equipment(models.Model):
    """
    Model untuk peralatan hiking yang bisa disewa
    """
    
    CATEGORY_CHOICES = [
        ('TENT', 'Tenda'),
        ('BACKPACK', 'Tas Punggung'),
        ('SLEEPING_BAG', 'Kantong Tidur'),
        ('COOKING', 'Peralatan Memasak'),
        ('SAFETY', 'Perlengkapan Keselamatan'),
        ('CLOTHING', 'Pakaian'),
        ('FOOTWEAR', 'Alas Kaki'),
        ('LIGHTING', 'Penerangan'),
        ('OTHER', 'Lainnya'),
    ]
    
    CONDITION_CHOICES = [
        ('NEW', 'Baru'),
        ('GOOD', 'Baik'),
        ('USED', 'Terpakai'),
        ('DAMAGED', 'Rusak'),
    ]
    
    # Basic info
    name = models.CharField(
        max_length=100,
        help_text="Nama peralatan"
    )
    description = models.TextField(
        help_text="Deskripsi detail peralatan"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='OTHER',
        help_text="Kategori peralatan"
    )
    
    # Pricing
    daily_rental_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Harga sewa per hari"
    )
    
    # Stock management
    total_quantity = models.IntegerField(
        default=1,
        help_text="Jumlah total item yang tersedia"
    )
    available_quantity = models.IntegerField(
        default=1,
        help_text="Jumlah item yang tersedia untuk disewa"
    )
    
    # Condition
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='GOOD',
        help_text="Kondisi peralatan"
    )
    
    # Additional info
    weight = models.FloatField(
        null=True,
        blank=True,
        help_text="Berat dalam kg"
    )
    size = models.CharField(
        max_length=50,
        blank=True,
        help_text="Ukuran (e.g., S, M, L, XL atau cm)"
    )
    color = models.CharField(
        max_length=50,
        blank=True,
        help_text="Warna peralatan"
    )
    
    # Image
    image = models.ImageField(
        upload_to='equipment/',
        null=True,
        blank=True,
        help_text="Foto peralatan"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Meta
    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.category})"
    
    def is_available(self):
        """Check apakah peralatan tersedia untuk disewa"""
        return self.available_quantity > 0
    
    def get_category_display_id(self):
        """Return ID dari kategori"""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)