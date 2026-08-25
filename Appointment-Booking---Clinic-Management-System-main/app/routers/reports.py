from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin"))
):
    today = date.today()

    # Total patients
    total_patients = db.query(Patient).count()

    # Total doctors
    total_doctors = db.query(Doctor).count()

    # Today's appointments
    todays_appointments = db.query(Appointment).filter(
        Appointment.appointment_date == today
    ).count()

    # Upcoming appointments
    upcoming_appointments = db.query(Appointment).filter(
        Appointment.appointment_date > today,
        Appointment.status != "Cancelled"
    ).count()

    # Completed appointments
    completed_appointments = db.query(Appointment).filter(
        Appointment.status == "Completed"
    ).count()

    # Cancelled appointments
    cancelled_appointments = db.query(Appointment).filter(
        Appointment.status == "Cancelled"
    ).count()

    # Most visited doctor
    most_visited = (
        db.query(
            Doctor.full_name,
            func.count(Appointment.id).label(
                "appointment_count"
            )
        )
        .join(
            Appointment,
            Appointment.doctor_id == Doctor.id
        )
        .group_by(
            Doctor.id,
            Doctor.full_name
        )
        .order_by(
            func.count(Appointment.id).desc()
        )
        .first()
    )

    # Average daily appointments
    first_appointment = db.query(
        func.min(Appointment.appointment_date)
    ).scalar()

    if first_appointment:
        days = (today - first_appointment).days + 1

        total_appointments = db.query(
            Appointment
        ).count()

        average_daily_appointments = round(
            total_appointments / days,
            2
        )
    else:
        average_daily_appointments = 0

    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "todays_appointments": todays_appointments,
        "upcoming_appointments": upcoming_appointments,
        "completed_appointments": completed_appointments,
        "cancelled_appointments": cancelled_appointments,
        "most_visited_doctor": (
            most_visited.full_name
            if most_visited
            else None
        ),
        "average_daily_appointments":
            average_daily_appointments
    }


@router.get("/appointments")
def appointment_report(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin"))
):
    appointments = db.query(Appointment).all()

    return {
        "total": len(appointments),
        "appointments": appointments
    }


@router.get("/doctors")
def doctor_report(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin"))
):
    doctors = db.query(Doctor).all()

    result = []

    for doctor in doctors:

        appointment_count = db.query(
            Appointment
        ).filter(
            Appointment.doctor_id == doctor.id
        ).count()

        result.append({
            "doctor_id": doctor.id,
            "doctor_name": doctor.full_name,
            "specialization": doctor.specialization,
            "total_appointments": appointment_count
        })

    return result