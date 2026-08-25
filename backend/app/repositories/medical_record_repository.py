from sqlalchemy.orm import Session
from app.models.medical_record import MedicalRecord
from app.repositories.base import BaseRepository


class MedicalRecordRepository(BaseRepository[MedicalRecord]):
    def __init__(self, db: Session):
        super().__init__(db, MedicalRecord)
