from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import require_role
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("", response_model=PatientResponse, status_code=201)
def create_patient(data: PatientCreate, db: Session = Depends(get_db), current_user=Depends(require_role("Admin","Receptionist"))):
    return PatientService(db).create(data)

@router.get("", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db), current_user=Depends(require_role("Admin","Doctor","Receptionist"))):
    return db.query(Patient).order_by(Patient.id.desc()).all()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db), current_user=Depends(require_role("Admin","Doctor","Receptionist"))):
    patient=db.query(Patient).filter(Patient.id==patient_id).first()
    if not patient: raise HTTPException(404,"Patient not found")
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, data: PatientCreate, db: Session = Depends(get_db), current_user=Depends(require_role("Admin","Receptionist"))):
    return PatientService(db).update(patient_id,data)

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db), current_user=Depends(require_role("Admin"))):
    PatientService(db).delete(patient_id)
    return {"message":"Patient deleted successfully"}
