from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.repositories.base import BaseRepository


class PatientRepository(BaseRepository[Patient]):
    def __init__(self, db: Session):
        super().__init__(db, Patient)

    def by_phone(self, phone: str):
        return self.db.query(Patient).filter(Patient.phone == phone).first()
