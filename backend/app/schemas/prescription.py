from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class PrescriptionCreate(BaseModel):
    appointment_id: int
    diagnosis: str = Field(min_length=2)
    medicines: str = Field(min_length=2)
    dosage: str = Field(min_length=2)
    instructions: str | None = None
    follow_up_date: date | None = None


class PrescriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    appointment_id: int
    patient_id: int
    doctor_id: int
    diagnosis: str
    medicines: str
    dosage: str
    instructions: str | None
    follow_up_date: date | None
