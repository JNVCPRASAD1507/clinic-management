import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.appointment import Appointment
from app.models.audit_log import AuditLog
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AppointmentRepository(db)

    def create(self, data: AppointmentCreate) -> Appointment:
        if not self.db.query(Patient).filter(Patient.id == data.patient_id).first():
            raise HTTPException(404, "Patient not found")
        if not self.db.query(Doctor).filter(Doctor.id == data.doctor_id).first():
            raise HTTPException(404, "Doctor not found")
        if self.repo.booked(data.doctor_id, data.appointment_date, data.time_slot):
            raise HTTPException(400, "Doctor is already booked for this time slot")
        appointment = Appointment(
            appointment_number=f"APT-{uuid.uuid4().hex[:8].upper()}",
            status="Scheduled",
            **data.model_dump(),
        )
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def update(self, appointment_id: int, data: AppointmentUpdate, user_id: int, user_role: str) -> Appointment:
        appointment = self.repo.get(appointment_id)
        if not appointment:
            raise HTTPException(404, "Appointment not found")
        if user_role == "Doctor":
            doctor = self.db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
            if not doctor or doctor.user_id != user_id:
                raise HTTPException(403, "Not authorized to update this appointment")
        updates = data.model_dump(exclude_unset=True)
        new_date = updates.get("appointment_date", appointment.appointment_date)
        new_time = updates.get("time_slot", appointment.time_slot)
        if self.repo.booked(appointment.doctor_id, new_date, new_time, appointment.id):
            raise HTTPException(400, "Doctor is already booked for this time slot")
        old = (appointment.status, appointment.appointment_date, appointment.time_slot)
        for key, value in updates.items():
            setattr(appointment, key, value)
        self.db.commit()
        self.db.refresh(appointment)
        self.db.add(AuditLog(
            user_id=user_id, appointment_id=appointment.id,
            action="APPOINTMENT_UPDATED",
            description=f"Appointment {appointment.appointment_number} updated. Status: {old[0]} -> {appointment.status}, Date: {old[1]} -> {appointment.appointment_date}, Time: {old[2]} -> {appointment.time_slot}",
        ))
        self.db.commit()
        return appointment

    def cancel(self, appointment_id: int, user_id: int) -> None:
        appointment = self.repo.get(appointment_id)
        if not appointment:
            raise HTTPException(404, "Appointment not found")
        appointment.status = "Cancelled"
        self.db.commit()
        self.db.add(AuditLog(
            user_id=user_id, appointment_id=appointment.id,
            action="APPOINTMENT_CANCELLED",
            description=f"Appointment {appointment.appointment_number} was cancelled",
        ))
        self.db.commit()
