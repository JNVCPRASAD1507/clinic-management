from typing import Optional

from pydantic import BaseModel, EmailStr


class DoctorCreate(BaseModel):
    user_id: Optional[int] = None
    full_name: str
    specialization: str
    qualification: str
    phone: str
    email: EmailStr
    consultation_fee: float
    available_timings: str


class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True