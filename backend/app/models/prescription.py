from datetime import datetime

from sqlalchemy import Column, Integer, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(
        Integer, ForeignKey("appointments.id"), nullable=False
    )
    patient_id = Column(
        Integer, ForeignKey("patients.id"), nullable=False
    )
    doctor_id = Column(
        Integer, ForeignKey("doctors.id"), nullable=False
    )
    diagnosis = Column(Text, nullable=False)
    medicines = Column(Text, nullable=False)
    dosage = Column(Text, nullable=False)
    instructions = Column(Text, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointment = relationship("Appointment", back_populates="prescription")
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")