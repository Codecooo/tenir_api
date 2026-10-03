from ninja import Router

from hiker.models import Hiker
from hiker.schema import HikerIn, HikerOut

router = Router()

@router.post("/new", response=HikerOut)
def create_hiker(payload: HikerIn):
    hiker = Hiker(
        first_name=payload.first_name, 
        last_name=payload.last_name,
        identity_number=payload.identity_number,
        phone_number=payload.phone_number,
        emergency_contact_name=payload.emergency_contact_name,
        emergency_contact_phone=payload.emergency_contact_phone
    )
    hiker.save()
    return hiker


@router.get("/{hiker_id}", response=HikerOut)
def get_hiker(hiker_id: int):
    return Hiker.objects.get(id=hiker_id)


@router.delete("/delete/{hiker_id}")
def delete_hiker(hiker_id: int):
    hiker = Hiker.objects.get(id=hiker_id)
    hiker.delete()
    return {"message": "Hiker deleted successfully."}


@router.put("/update/{hiker_id}", response=HikerOut)
def update_hiker(hiker_id: int, payload: HikerIn):
    hiker = Hiker.objects.get(id=hiker_id)
    hiker.first_name = payload.first_name
    hiker.last_name = payload.last_name
    hiker.identity_number = payload.identity_number
    hiker.phone_number = payload.phone_number
    hiker.emergency_contact_name = payload.emergency_contact_name
    hiker.emergency_contact_phone = payload.emergency_contact_phone
    hiker.save()
    return hiker