from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    qualification = Column(String(150), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    consultation_fee = Column(Float, nullable=False)
    available_timings = Column(String(255), nullable=False)

    user = relationship("User")

    appointments = relationship(
        "Appointment",
        back_populates="doctor"
    )

    prescriptions = relationship(
        "Prescription",
        back_populates="doctor"
    )