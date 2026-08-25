from datetime import date
import uuid

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.audit_log import AuditLog
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)
from app.dependencies import require_role
from app.services.notification_service import (
    send_appointment_confirmation,
    send_appointment_reminder
)


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_appointment(
    appointment_data: AppointmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Receptionist")
    )
):
    patient = db.query(Patient).filter(
        Patient.id == appointment_data.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == appointment_data.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Prevent double booking
    existing_appointment = db.query(Appointment).filter(
        Appointment.doctor_id == appointment_data.doctor_id,
        Appointment.appointment_date == appointment_data.appointment_date,
        Appointment.time_slot == appointment_data.time_slot,
        Appointment.status != "Cancelled"
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="Doctor is already booked for this time slot"
        )

    appointment = Appointment(
        appointment_number=f"APT-{uuid.uuid4().hex[:8].upper()}",
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        appointment_date=appointment_data.appointment_date,
        time_slot=appointment_data.time_slot,
        reason=appointment_data.reason,
        status="Scheduled"
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # Background task - appointment confirmation
    background_tasks.add_task(
        send_appointment_confirmation,
        patient.phone,
        appointment.appointment_number
    )

    # Background task - appointment reminder
    background_tasks.add_task(
        send_appointment_reminder,
        patient.phone,
        appointment.appointment_number
    )

    return appointment


@router.get(
    "",
    response_model=list[AppointmentResponse]
)
def get_appointments(
    patient_name: str | None = None,
    doctor_name: str | None = None,
    appointment_number: str | None = None,
    appointment_status: str | None = None,
    appointment_date: date | None = None,
    specialization: str | None = None,

    # Pagination
    page: int = 1,
    page_size: int = 10,

    # Sorting
    sort_by: str = "appointment_date",
    sort_order: str = "asc",

    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Doctor", "Receptionist")
    )
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be greater than or equal to 1"
        )

    if page_size < 1 or page_size > 100:
        raise HTTPException(
            status_code=400,
            detail="Page size must be between 1 and 100"
        )

    allowed_sort_fields = {
        "id": Appointment.id,
        "appointment_date": Appointment.appointment_date,
        "appointment_number": Appointment.appointment_number,
        "status": Appointment.status,
        "time_slot": Appointment.time_slot
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid sort_by. Allowed values: "
                "id, appointment_date, appointment_number, "
                "status, time_slot"
            )
        )

    if sort_order.lower() not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="sort_order must be 'asc' or 'desc'"
        )

    query = db.query(Appointment).join(
        Patient,
        Appointment.patient_id == Patient.id
    ).join(
        Doctor,
        Appointment.doctor_id == Doctor.id
    )

    # Doctor can see only assigned appointments
    if current_user.role == "Doctor":

        doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user.id
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor profile not found"
            )

        query = query.filter(
            Appointment.doctor_id == doctor.id
        )

    # Patient name filter
    if patient_name:
        query = query.filter(
            Patient.full_name.ilike(
                f"%{patient_name}%"
            )
        )

    # Doctor name filter
    if doctor_name:
        query = query.filter(
            Doctor.full_name.ilike(
                f"%{doctor_name}%"
            )
        )

    # Appointment number filter
    if appointment_number:
        query = query.filter(
            Appointment.appointment_number.ilike(
                f"%{appointment_number}%"
            )
        )

    # Appointment status filter
    if appointment_status:
        query = query.filter(
            Appointment.status == appointment_status
        )

    # Appointment date filter
    if appointment_date:
        query = query.filter(
            Appointment.appointment_date == appointment_date
        )

    # Specialization filter
    if specialization:
        query = query.filter(
            Doctor.specialization.ilike(
                f"%{specialization}%"
            )
        )

    # Sorting
    sort_column = allowed_sort_fields[sort_by]

    if sort_order.lower() == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    # Pagination
    offset = (page - 1) * page_size

    return query.offset(
        offset
    ).limit(
        page_size
    ).all()


@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Doctor", "Receptionist")
    )
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    # Doctor can view only their assigned appointment
    if current_user.role == "Doctor":

        doctor = db.query(Doctor).filter(
            Doctor.id == appointment.doctor_id
        ).first()

        if not doctor or doctor.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view this appointment"
            )

    return appointment


@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Receptionist", "Doctor")
    )
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    # Doctor can update only their assigned appointment
    if current_user.role == "Doctor":

        doctor = db.query(Doctor).filter(
            Doctor.id == appointment.doctor_id
        ).first()

        if not doctor or doctor.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to update this appointment"
            )

    update_data = appointment_data.model_dump(
        exclude_unset=True
    )

    # Check double booking when date/time is changed
    new_date = update_data.get(
        "appointment_date",
        appointment.appointment_date
    )

    new_time = update_data.get(
        "time_slot",
        appointment.time_slot
    )

    if (
        new_date != appointment.appointment_date
        or new_time != appointment.time_slot
    ):
        existing_appointment = db.query(Appointment).filter(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_date == new_date,
            Appointment.time_slot == new_time,
            Appointment.status != "Cancelled",
            Appointment.id != appointment.id
        ).first()

        if existing_appointment:
            raise HTTPException(
                status_code=400,
                detail="Doctor is already booked for this time slot"
            )

    # Store old values for audit log
    old_status = appointment.status
    old_date = appointment.appointment_date
    old_time = appointment.time_slot

    for key, value in update_data.items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)

    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        appointment_id=appointment.id,
        action="APPOINTMENT_UPDATED",
        description=(
            f"Appointment {appointment.appointment_number} updated. "
            f"Status: {old_status} -> {appointment.status}, "
            f"Date: {old_date} -> {appointment.appointment_date}, "
            f"Time: {old_time} -> {appointment.time_slot}"
        )
    )

    db.add(audit_log)
    db.commit()

    return appointment


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Receptionist")
    )
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.status = "Cancelled"

    db.commit()
    db.refresh(appointment)

    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        appointment_id=appointment.id,
        action="APPOINTMENT_CANCELLED",
        description=(
            f"Appointment "
            f"{appointment.appointment_number} "
            f"was cancelled"
        )
    )

    db.add(audit_log)
    db.commit()

    return {
        "message": "Appointment cancelled successfully"
    }