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
from app.models.prescription import Prescription
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionResponse
)
from app.dependencies import require_role
from app.services.notification_service import (
    send_prescription_notification
)


router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)


@router.post(
    "",
    response_model=PrescriptionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_prescription(
    prescription_data: PrescriptionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Doctor"))
):
    appointment = db.query(Appointment).filter(
        Appointment.id == prescription_data.appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment.status != "Completed":
        raise HTTPException(
            status_code=400,
            detail="Prescription can only be created for completed appointments"
        )

    existing = db.query(Prescription).filter(
        Prescription.appointment_id ==
        prescription_data.appointment_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Prescription already exists for this appointment"
        )

    prescription = Prescription(
        appointment_id=appointment.id,
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        diagnosis=prescription_data.diagnosis,
        medicines=prescription_data.medicines,
        dosage=prescription_data.dosage,
        instructions=prescription_data.instructions,
        follow_up_date=prescription_data.follow_up_date
    )

    db.add(prescription)
    db.commit()
    db.refresh(prescription)

    background_tasks.add_task(
        send_prescription_notification,
        appointment.patient.phone,
        prescription.id
    )

    return prescription


@router.get(
    "",
    response_model=list[PrescriptionResponse]
)
def get_prescriptions(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Doctor")
    )
):
    return db.query(Prescription).all()


@router.get(
    "/{prescription_id}",
    response_model=PrescriptionResponse
)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Doctor")
    )
):
    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id
    ).first()

    if not prescription:
        raise HTTPException(
            status_code=404,
            detail="Prescription not found"
        )

    return prescription


@router.put(
    "/{prescription_id}",
    response_model=PrescriptionResponse
)
def update_prescription(
    prescription_id: int,
    prescription_data: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Doctor"))
):
    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id
    ).first()

    if not prescription:
        raise HTTPException(
            status_code=404,
            detail="Prescription not found"
        )

    update_data = prescription_data.model_dump(
        exclude={"appointment_id"},
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(prescription, key, value)

    db.commit()
    db.refresh(prescription)

    return prescription