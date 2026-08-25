from sqlalchemy.orm import Session
from app.models.prescription import Prescription
from app.repositories.base import BaseRepository


class PrescriptionRepository(BaseRepository[Prescription]):
    def __init__(self, db: Session):
        super().__init__(db, Prescription)
