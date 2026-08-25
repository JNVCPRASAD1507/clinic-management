from datetime import date
from typing import Literal

from pydantic import BaseModel


AppointmentStatus = Literal[
    "Scheduled",
    "Confirmed",
    "Completed",
    "Cancelled",
    "No Show"
]


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    time_slot: str
    reason: str


class AppointmentUpdate(BaseModel):
    appointment_date: date | None = None
    time_slot: str | None = None
    reason: str | None = None
    status: AppointmentStatus | None = None


class AppointmentResponse(BaseModel):
    id: int
    appointment_number: str
    patient_id: int
    doctor_id: int
    appointment_date: date
    time_slot: str
    reason: str
    status: AppointmentStatus

    class Config:
        from_attributes = True