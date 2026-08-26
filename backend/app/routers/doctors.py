from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import require_role
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("", response_model=DoctorResponse, status_code=201)
def create_doctor(
    data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin")),
):
    return DoctorService(db).create(data)


@router.get("", response_model=list[DoctorResponse])
def get_doctors(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin", "Doctor", "Receptionist")),
):
    return db.query(Doctor).order_by(Doctor.id.desc()).all()


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin", "Doctor", "Receptionist")),
):
    d = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not d:
        raise HTTPException(404, "Doctor not found")
    return d


@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin")),
):
    return DoctorService(db).update(doctor_id, data)


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin")),
):
    d = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not d:
        raise HTTPException(404, "Doctor not found")
    db.delete(d)
    db.commit()
    return {"message": "Doctor deleted successfully"}
