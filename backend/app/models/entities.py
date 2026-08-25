from datetime import date, datetime, time
from enum import Enum
from sqlalchemy import Boolean, Date, DateTime, Enum as SAEnum, Float, ForeignKey, Integer, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class UserRole(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    RECEPTIONIST = "receptionist"

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.RECEPTIONIST)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), index=True)
    specialization: Mapped[str] = mapped_column(String(120), index=True)
    qualification: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    consultation_fee: Mapped[float] = mapped_column(Float, default=0)
    available_timings: Mapped[str] = mapped_column(Text, default="09:00-17:00")

class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), index=True)
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(30), index=True)
    address: Mapped[str] = mapped_column(Text)
    blood_group: Mapped[str] = mapped_column(String(10), default="Unknown")
    emergency_contact: Mapped[str] = mapped_column(String(30))

class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (UniqueConstraint("doctor_id", "appointment_date", "time_slot", name="uq_doctor_slot"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_number: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), index=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id", ondelete="CASCADE"), index=True)
    appointment_date: Mapped[date] = mapped_column(Date, index=True)
    time_slot: Mapped[time] = mapped_column(Time)
    reason_for_visit: Mapped[str] = mapped_column(Text)
    status: Mapped[AppointmentStatus] = mapped_column(SAEnum(AppointmentStatus), default=AppointmentStatus.SCHEDULED, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    patient: Mapped[Patient] = relationship()
    doctor: Mapped[Doctor] = relationship()

class Prescription(Base):
    __tablename__ = "prescriptions"
    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id", ondelete="CASCADE"))
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), index=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id", ondelete="CASCADE"), index=True)
    diagnosis: Mapped[str] = mapped_column(Text)
    medicines: Mapped[str] = mapped_column(Text)
    dosage: Mapped[str] = mapped_column(Text)
    instructions: Mapped[str] = mapped_column(Text)
    follow_up_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), index=True)
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    content_type: Mapped[str] = mapped_column(String(100))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id", ondelete="CASCADE"))
    action: Mapped[str] = mapped_column(String(100))
    old_status: Mapped[str | None] = mapped_column(String(30))
    new_status: Mapped[str | None] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
