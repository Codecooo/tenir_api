from ninja import Router
from django.shortcuts import get_object_or_404
from equipment.models import Equipment
from equipment.serializers import EquipmentSchema, EquipmentCreateSchema, EquipmentUpdateSchema

router = Router()

# ============================================
# GET ENDPOINTS
# ============================================

@router.get("/equipment", response=list[EquipmentSchema], tags=["Equipment"])
def list_equipment(request, category: str = None, available_only: bool = False):
    """
    Get semua equipment
    Optional query params:
    - category: Filter by category (e.g., "TENT", "BACKPACK")
    - available_only: Hanya tampilkan yang tersedia (true/false)
    """
    queryset = Equipment.objects.all()
    
    if category:
        queryset = queryset.filter(category=category)
    
    if available_only:
        queryset = queryset.filter(available_quantity__gt=0)
    
    return queryset


@router.get("/equipment/{equipment_id}", response=EquipmentSchema, tags=["Equipment"])
def get_equipment(request, equipment_id: int):
    """
    Get detail equipment by ID
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    return equipment


@router.get("/equipment/categories", tags=["Equipment"])
def get_equipment_categories(request):
    """
    Get daftar semua kategori equipment
    """
    categories = [
        {"value": "TENT", "label": "Tenda"},
        {"value": "BACKPACK", "label": "Tas Punggung"},
        {"value": "SLEEPING_BAG", "label": "Kantong Tidur"},
        {"value": "COOKING", "label": "Peralatan Memasak"},
        {"value": "SAFETY", "label": "Perlengkapan Keselamatan"},
        {"value": "CLOTHING", "label": "Pakaian"},
        {"value": "FOOTWEAR", "label": "Alas Kaki"},
        {"value": "LIGHTING", "label": "Penerangan"},
        {"value": "OTHER", "label": "Lainnya"},
    ]
    return categories


# ============================================
# POST ENDPOINTS
# ============================================

@router.post("/equipment", response=EquipmentSchema, tags=["Equipment"])
def create_equipment(request, payload: EquipmentCreateSchema):
    """
    Create equipment baru
    Required fields:
    - name
    - description
    - category (TENT, BACKPACK, SLEEPING_BAG, etc)
    - daily_rental_price
    - total_quantity
    - available_quantity
    - condition (NEW, GOOD, USED, DAMAGED)
    """
    equipment = Equipment.objects.create(
        name=payload.name,
        description=payload.description,
        category=payload.category,
        daily_rental_price=payload.daily_rental_price,
        total_quantity=payload.total_quantity,
        available_quantity=payload.available_quantity,
        condition=payload.condition,
        weight=payload.weight,
        size=payload.size,
        color=payload.color,
    )
    return equipment


# ============================================
# PUT ENDPOINTS (Update)
# ============================================

@router.put("/equipment/{equipment_id}", response=EquipmentSchema, tags=["Equipment"])
def update_equipment(request, equipment_id: int, payload: EquipmentUpdateSchema):
    """
    Update equipment by ID
    Send only fields yang mau diubah
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    # Update hanya field yang dikirim (bukan None)
    update_data = payload.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            setattr(equipment, field, value)
    
    equipment.save()
    return equipment


# ============================================
# DELETE ENDPOINTS
# ============================================

@router.delete("/equipment/{equipment_id}", tags=["Equipment"])
def delete_equipment(request, equipment_id: int):
    """
    Delete equipment by ID
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    equipment_name = equipment.name
    equipment.delete()
    return {"message": f"Equipment '{equipment_name}' deleted successfully"}


# ============================================
# UTILITY ENDPOINTS
# ============================================

@router.post("/equipment/{equipment_id}/update-stock", response=EquipmentSchema, tags=["Equipment"])
def update_equipment_stock(request, equipment_id: int, available_quantity: int):
    """
    Update available quantity equipment
    Useful untuk manage stock saat ada rental/return
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    if available_quantity > equipment.total_quantity:
        return {
            "error": f"Available quantity tidak boleh lebih dari total quantity ({equipment.total_quantity})"
        }, 400
    
    if available_quantity < 0:
        return {"error": "Available quantity tidak boleh negatif"}, 400
    
    equipment.available_quantity = available_quantity
    equipment.save()
    return equipment