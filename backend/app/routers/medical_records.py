import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app.schemas.medical_record import MedicalRecordResponse


router = APIRouter(
    prefix="/medical-records",
    tags=["Medical Records"]
)


UPLOAD_DIR = "uploads/medical_records"


ALLOWED_TYPES = {
    "application/pdf": "pdf",
    "image/jpeg": "jpg",
    "image/png": "png",
}


@router.post(
    "/upload",
    response_model=MedicalRecordResponse,
    status_code=status.HTTP_201_CREATED
)
def upload_medical_record(
    patient_id: int,
    file: UploadFile = File(...),
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

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG and PNG files are allowed"
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    extension = ALLOWED_TYPES[file.content_type]
    unique_name = f"{uuid.uuid4().hex}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    record = MedicalRecord(
        patient_id=patient_id,
        file_name=file.filename,
        file_path=file_path,
        file_type=extension
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get(
    "/{patient_id}",
    response_model=list[MedicalRecordResponse]
)
def get_patient_medical_records(
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

    return db.query(MedicalRecord).filter(
        MedicalRecord.patient_id == patient_id
    ).all()


@router.get(
    "/download/{record_id}"
)
def download_medical_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("Admin", "Doctor", "Receptionist")
    )
):
    record = db.query(MedicalRecord).filter(
        MedicalRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )

    if not os.path.exists(record.file_path):
        raise HTTPException(
            status_code=404,
            detail="Medical report file not found"
        )

    return FileResponse(
        path=record.file_path,
        filename=record.file_name,
        media_type="application/octet-stream"
    )