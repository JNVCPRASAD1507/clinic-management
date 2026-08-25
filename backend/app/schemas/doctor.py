from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DoctorCreate(BaseModel):
    user_id: int | None = None
    full_name: str = Field(min_length=2, max_length=100)
    specialization: str
    qualification: str
    phone: str
    email: EmailStr
    consultation_fee: float = Field(ge=0)
    available_timings: str


class DoctorResponse(DoctorCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
