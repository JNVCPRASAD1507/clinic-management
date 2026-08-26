import os
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.dependencies import require_role
from app.models.medical_record import MedicalRecord
from app.schemas.medical_record import MedicalRecordResponse
from app.services.medical_record_service import MedicalRecordService

router = APIRouter(prefix="/medical-records", tags=["Medical Records"])


@router.post("/upload", response_model=MedicalRecordResponse, status_code=201)
def upload_medical_record(
    patient_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin", "Doctor", "Receptionist")),
):
    return MedicalRecordService(db).upload(patient_id, file)


@router.get("/{patient_id}", response_model=list[MedicalRecordResponse])
def get_patient_medical_records(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin", "Doctor", "Receptionist")),
):
    from app.models.patient import Patient

    if not db.query(Patient).filter(Patient.id == patient_id).first():
        raise HTTPException(404, "Patient not found")
    return (
        db.query(MedicalRecord)
        .filter(MedicalRecord.patient_id == patient_id)
        .order_by(MedicalRecord.id.desc())
        .all()
    )


@router.get("/download/{record_id}")
def download_medical_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin", "Doctor", "Receptionist")),
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(404, "Medical record not found")
    if not os.path.exists(record.file_path):
        raise HTTPException(404, "Medical report file not found")
    return FileResponse(
        record.file_path,
        filename=record.file_name,
        media_type="application/octet-stream",
    )
