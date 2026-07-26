from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class MedicineBase(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None

class MedicineCreate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id: int
    prescription_id: int

    model_config = ConfigDict(from_attributes=True)

class PrescriptionBase(BaseModel):
    doctor_name: Optional[str] = None
    clinic_name: Optional[str] = None
    date: datetime

class PrescriptionCreate(BaseModel):
    doctor_name: Optional[str] = None
    clinic_name: Optional[str] = None
    date: datetime = datetime.now()
    medicines: List[MedicineCreate] = []

class PrescriptionResponse(PrescriptionBase):
    id: int
    user_id: int
    file_path: Optional[str] = None
    raw_text: Optional[str] = None
    summary: Optional[str] = None
    medicines: List[MedicineResponse] = []

    model_config = ConfigDict(from_attributes=True)
