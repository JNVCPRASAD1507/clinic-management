from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models.entities import AppointmentStatus, UserRole

class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6)
    role: UserRole = UserRole.RECEPTIONIST
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class DoctorBase(BaseModel):
    full_name: str
    specialization: str
    qualification: str
    phone_number: str
    email: EmailStr
    consultation_fee: float = Field(ge=0)
    available_timings: str
class DoctorCreate(DoctorBase): pass
class DoctorUpdate(DoctorBase): pass
class DoctorOut(DoctorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PatientBase(BaseModel):
    full_name: str
    age: int = Field(ge=0, le=130)
    gender: str
    phone_number: str
    address: str
    blood_group: str = "Unknown"
    emergency_contact: str
class PatientCreate(PatientBase): pass
class PatientUpdate(PatientBase): pass
class PatientOut(PatientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    time_slot: time
    reason_for_visit: str
class AppointmentUpdate(BaseModel):
    patient_id: int | None = None
    doctor_id: int | None = None
    appointment_date: date | None = None
    time_slot: time | None = None
    reason_for_visit: str | None = None
    status: AppointmentStatus | None = None
class AppointmentOut(BaseModel):
    id: int
    appointment_number: str
    patient_id: int
    doctor_id: int
    appointment_date: date
    time_slot: time
    reason_for_visit: str
    status: AppointmentStatus
    patient_name: str | None = None
    doctor_name: str | None = None
    model_config = ConfigDict(from_attributes=True)

class PrescriptionCreate(BaseModel):
    appointment_id: int
    diagnosis: str
    medicines: str
    dosage: str
    instructions: str
    follow_up_date: date | None = None
class PrescriptionUpdate(BaseModel):
    diagnosis: str | None = None
    medicines: str | None = None
    dosage: str | None = None
    instructions: str | None = None
    follow_up_date: date | None = None
class PrescriptionOut(BaseModel):
    id: int
    appointment_id: int
    patient_id: int
    doctor_id: int
    diagnosis: str
    medicines: str
    dosage: str
    instructions: str
    follow_up_date: date | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
