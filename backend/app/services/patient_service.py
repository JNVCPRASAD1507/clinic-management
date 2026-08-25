from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.patient import Patient
from app.schemas.patient import PatientCreate


class PatientService:
    def __init__(self, db: Session): self.db = db

    def create(self, data: PatientCreate):
        patient = Patient(**data.model_dump())
        self.db.add(patient); self.db.commit(); self.db.refresh(patient)
        return patient

    def update(self, patient_id: int, data: PatientCreate):
        patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient: raise HTTPException(404, "Patient not found")
        for key, value in data.model_dump().items(): setattr(patient, key, value)
        self.db.commit(); self.db.refresh(patient)
        return patient

    def delete(self, patient_id: int):
        patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient: raise HTTPException(404, "Patient not found")
        self.db.delete(patient); self.db.commit()
