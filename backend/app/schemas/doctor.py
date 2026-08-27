from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DoctorCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    specialization: str
    qualification: str
    phone: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    consultation_fee: float = Field(ge=0)
    available_timings: str


class DoctorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None = None
    full_name: str
    specialization: str
    qualification: str
    phone: str
    email: EmailStr
    consultation_fee: float
    available_timings: str
    
# class DoctorUpdate(BaseModel):
#     full_name: str = Field(min_length=2, max_length=100)
#     specialization: str
#     qualification: str
#     phone: str
#     email: EmailStr
#     password: str | None = Field(default=None, min_length=8, max_length=128)
#     consultation_fee: float = Field(ge=0)
#     available_timings: str
