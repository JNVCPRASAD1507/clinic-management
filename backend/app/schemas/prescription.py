from datetime import date
from pydantic import BaseModel


class PrescriptionCreate(BaseModel):
    appointment_id: int
    diagnosis: str
    medicines: str
    dosage: str
    instructions: str | None = None
    follow_up_date: date | None = None


class PrescriptionResponse(BaseModel):
    id: int
    appointment_id: int
    patient_id: int
    doctor_id: int
    diagnosis: str
    medicines: str
    dosage: str
    instructions: str | None
    follow_up_date: date | None

    class Config:
        from_attributes = True