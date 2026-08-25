from pydantic import BaseModel, ConfigDict, Field


class PatientCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=130)
    gender: str
    phone: str
    address: str
    blood_group: str | None = None
    emergency_contact: str


class PatientResponse(PatientCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
