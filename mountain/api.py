## hello gemini this is a test run review this code

from ninja import Router
from django.shortcuts import get_object_or_404
from mountain.models import Mountain
from mountain.serializers import MountainSchema, MountainCreateSchema, MountainUpdateSchema

router = Router()

# ============================================
# GET ENDPOINTS
# ============================================

@router.get("/mountains", response=list[MountainSchema], tags=["Mountain"])
def list_mountains(request, region: str = None, difficulty: str = None):
    """
    Get semua mountains
    Optional query params:
    - region: Filter by region (e.g., "JAWA_TIMUR")
    - difficulty: Filter by difficulty level (e.g., "EASY")
    """
    queryset = Mountain.objects.all()
    
    if region:
        queryset = queryset.filter(region=region)
    
    if difficulty:
        queryset = queryset.filter(difficulty_level=difficulty)
    
    return queryset


@router.get("/mountains/{mountain_id}", response=MountainSchema, tags=["Mountain"])
def get_mountain(request, mountain_id: int):
    """
    Get detail mountain by ID
    """
    mountain = get_object_or_404(Mountain, id=mountain_id)
    return mountain


# ============================================
# POST ENDPOINTS
# ============================================

@router.post("/mountains", response=MountainSchema, tags=["Mountain"])
def create_mountain(request, payload: MountainCreateSchema):
    """
    Create mountain baru
    Required fields:
    - name
    - location
    - description
    - height
    - difficulty_level (EASY, MODERATE, CHALLENGING, EXPERT)
    - region
    - indonesian_weekday_price
    - indonesian_weekend_price
    - international_weekday_price
    - international_weekend_price
    - alert_level (SIAGA, WASPADA, AWAS)
    """
    mountain = Mountain.objects.create(
        name=payload.name,
        location=payload.location,
        description=payload.description,
        height=payload.height,
        difficulty_level=payload.difficulty_level,
        region=payload.region,
        indonesian_weekday_price=payload.indonesian_weekday_price,
        indonesian_weekend_price=payload.indonesian_weekend_price,
        international_weekday_price=payload.international_weekday_price,
        international_weekend_price=payload.international_weekend_price,
        alert_level=payload.alert_level,
    )
    return mountain


# ============================================
# PUT ENDPOINTS (Update)
# ============================================

@router.put("/mountains/{mountain_id}", response=MountainSchema, tags=["Mountain"])
def update_mountain(request, mountain_id: int, payload: MountainUpdateSchema):
    """
    Update mountain by ID
    Send only fields yang mau diubah
    """
    mountain = get_object_or_404(Mountain, id=mountain_id)
    
    # Update hanya field yang dikirim (bukan None)
    update_data = payload.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            setattr(mountain, field, value)
    
    mountain.save()
    return mountain


# ============================================
# DELETE ENDPOINTS
# ============================================

@router.delete("/mountains/{mountain_id}", tags=["Mountain"])
def delete_mountain(request, mountain_id: int):
    """
    Delete mountain by ID
    """
    mountain = get_object_or_404(Mountain, id=mountain_id)
    mountain_name = mountain.name
    mountain.delete()
    return {"message": f"Mountain '{mountain_name}' deleted successfully"}


# ============================================
# HELLO TEST ENDPOINT (Keep existing)
# ============================================

@router.get("/hello", tags=["Test"])
def hello(request):
    """
    Test endpoint
    """
    mountain = Mountain.objects.first()
    return {"message": "Hello, World!", "mountain": mountain}