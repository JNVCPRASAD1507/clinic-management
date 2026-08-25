from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.dependencies import require_role


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post(
    "",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED
)
def create_doctor(
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin"))
):
    user = db.query(User).filter(
        User.id == doctor_data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "Doctor":
        raise HTTPException(
            status_code=400,
            detail="Selected user must have Doctor role"
        )

    existing_doctor_user = db.query(Doctor).filter(
        Doctor.user_id == doctor_data.user_id
    ).first()

    if existing_doctor_user:
        raise HTTPException(
            status_code=400,
            detail="Doctor profile already exists for this user"
        )

    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor_data.email
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor with this email already exists"
        )

    doctor = Doctor(
        **doctor_data.model_dump()
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


@router.get(
    "",
    response_model=list[DoctorResponse]
)
def get_doctors(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Doctor", "Receptionist")
    )
):
    return db.query(Doctor).all()


@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Doctor", "Receptionist")
    )
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def update_doctor(
    doctor_id: int,
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin"))
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    user = db.query(User).filter(
        User.id == doctor_data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "Doctor":
        raise HTTPException(
            status_code=400,
            detail="Selected user must have Doctor role"
        )

    for key, value in doctor_data.model_dump().items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin"))
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    db.delete(doctor)
    db.commit()

    return {
        "message": "Doctor deleted successfully"
    }