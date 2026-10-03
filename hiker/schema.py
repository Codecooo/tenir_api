from ninja import ModelSchema
from hiker.models import Hiker

class HikerIn(ModelSchema):
    class Meta:
        model = Hiker
        fields = ['first_name', 'last_name', 'identity_number', 'phone_number', 'emergency_contact_name', 'emergency_contact_phone', 'medical_notes']

class HikerOut(ModelSchema):
    class Meta:
        model = Hiker
        fields = '__all__'