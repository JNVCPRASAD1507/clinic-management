from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse
from app.dependencies import require_role


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED
)
def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin", "Receptionist"))
):
    patient = Patient(**patient_data.model_dump())

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


@router.get("", response_model=list[PatientResponse])
def get_patients(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Doctor", "Receptionist")
    )
):
    return db.query(Patient).all()


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Doctor", "Receptionist")
    )
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Receptionist")
    )
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    for key, value in patient_data.model_dump().items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return patient


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin"))
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully"
    }