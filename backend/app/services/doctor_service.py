from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.doctor import DoctorCreate


class DoctorService:
    def __init__(self, db: Session):
        self.db = db

    def validate_user(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(404, "User not found")
        if user.role != "Doctor":
            raise HTTPException(400, "Selected user must have Doctor role")
        return user

    def create(self, data: DoctorCreate):
        if data.user_id is not None:
            self.validate_user(data.user_id)
        if self.db.query(Doctor).filter(Doctor.email == data.email).first():
            raise HTTPException(400, "Doctor with this email already exists")
        doctor = Doctor(**data.model_dump())
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        return doctor

    def update(self, doctor_id, data):
        doctor = self.db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(404, "Doctor not found")
        if data.user_id is not None:
            self.validate_user(data.user_id)
        for key, value in data.model_dump().items():
            setattr(doctor, key, value)
        self.db.commit()
        self.db.refresh(doctor)
        return doctor
