from pydantic import BaseModel


class PatientCreate(BaseModel):
    full_name: str
    age: int
    gender: str
    phone: str
    address: str
    blood_group: str | None = None
    emergency_contact: str


class PatientResponse(PatientCreate):
    id: int

    class Config:
        from_attributes = True