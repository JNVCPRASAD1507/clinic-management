from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from app.repositories.base import BaseRepository


class AppointmentRepository(BaseRepository[Appointment]):
    def __init__(self, db: Session):
        super().__init__(db, Appointment)

    def booked(self, doctor_id, appointment_date, time_slot, exclude_id=None):
        q = self.db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appointment_date,
            Appointment.time_slot == time_slot,
            Appointment.status != "Cancelled",
        )
        if exclude_id:
            q = q.filter(Appointment.id != exclude_id)
        return q.first()
