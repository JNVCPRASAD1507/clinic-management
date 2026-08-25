import os, uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.medical_record import MedicalRecord
from app.models.patient import Patient

ALLOWED_TYPES = {"application/pdf": "pdf", "image/jpeg": "jpg", "image/png": "png"}

class MedicalRecordService:
    def __init__(self, db: Session): self.db = db

    def upload(self, patient_id: int, file: UploadFile):
        if not self.db.query(Patient).filter(Patient.id == patient_id).first():
            raise HTTPException(404, "Patient not found")
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(400, "Only PDF, JPG and PNG files are allowed")
        os.makedirs(settings.upload_dir, exist_ok=True)
        extension = ALLOWED_TYPES[file.content_type]
        unique_name = f"{uuid.uuid4().hex}.{extension}"
        path = os.path.join(settings.upload_dir, unique_name)
        with open(path, "wb") as buffer:
            buffer.write(file.file.read())
        record = MedicalRecord(patient_id=patient_id, file_name=file.filename or unique_name, file_path=path, file_type=extension)
        self.db.add(record); self.db.commit(); self.db.refresh(record)
        return record
