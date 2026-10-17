from typing import List

from ninja import Query, Router
from ninja.errors import HttpError

from mountain.models import Mountain
from mountain.schema import (
    ErrorOut,
    MountainDetailOut,
    MountainFilter,
    MountainListOut,
)

router = Router()


@router.get("", response=List[MountainListOut])
def list_mountains(request, filters: MountainFilter = Query(...)):
    """
    Get semua mountains.

    Optional query params:
    - region: Filter by region (e.g., "JAWA_TIMUR")
    - difficulty: Filter by difficulty level (e.g., "Gampang", "Normal", "Menantang", "Expert")
    """
    return filters.filter(Mountain.objects.all().order_by("id"))


@router.get(
    "/{mountain_id}",
    response={200: MountainDetailOut, 404: ErrorOut},
)
def get_mountain(request, mountain_id: int):
    """Get detail satu gunung beserta foto-fotonya."""
    try:
        return Mountain.objects.prefetch_related("pictures").get(id=mountain_id)
    except Mountain.DoesNotExist:
        raise HttpError(404, "Mountain not found")