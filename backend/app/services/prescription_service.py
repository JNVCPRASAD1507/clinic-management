from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.appointment import Appointment
from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionCreate


class PrescriptionService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: PrescriptionCreate):
        appointment = (
            self.db.query(Appointment)
            .filter(Appointment.id == data.appointment_id)
            .first()
        )
        if not appointment:
            raise HTTPException(404, "Appointment not found")
        if appointment.status != "Completed":
            raise HTTPException(
                400, "Prescription can only be created for completed appointments"
            )
        if (
            self.db.query(Prescription)
            .filter(Prescription.appointment_id == data.appointment_id)
            .first()
        ):
            raise HTTPException(400, "Prescription already exists for this appointment")
        prescription = Prescription(
            appointment_id=appointment.id,
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            **data.model_dump(exclude={"appointment_id"}),
        )
        self.db.add(prescription)
        self.db.commit()
        self.db.refresh(prescription)
        return prescription
