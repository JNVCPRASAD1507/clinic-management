from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.repositories.base import BaseRepository


class DoctorRepository(BaseRepository[Doctor]):
    def __init__(self, db: Session):
        super().__init__(db, Doctor)
