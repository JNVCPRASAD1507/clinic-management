from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models.doctor import Doctor
from app.models.user import User


class DoctorService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data):
        # Check whether a user already exists with this email
        existing_user = (
            self.db.query(User)
            .filter(User.email == data.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists",
            )

        # Check whether a doctor already exists with this email
        existing_doctor = (
            self.db.query(Doctor)
            .filter(Doctor.email == data.email)
            .first()
        )

        if existing_doctor:
            raise HTTPException(
                status_code=400,
                detail="Doctor with this email already exists",
            )

        try:
            # 1. Create login user
            user = User(
                full_name=data.full_name,
                email=data.email,
                hashed_password=hash_password(data.password),
                role="Doctor",
            )

            self.db.add(user)
            self.db.flush()

            # 2. Create doctor profile linked to the user
            doctor = Doctor(
                user_id=user.id,
                full_name=data.full_name,
                specialization=data.specialization,
                qualification=data.qualification,
                phone=data.phone,
                email=data.email,
                consultation_fee=data.consultation_fee,
                available_timings=data.available_timings,
            )

            self.db.add(doctor)
            self.db.commit()

            self.db.refresh(doctor)

            return doctor

        except Exception:
            self.db.rollback()
            raise

    def update(self, doctor_id, data):
        doctor = (
            self.db.query(Doctor)
            .filter(Doctor.id == doctor_id)
            .first()
        )

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found",
            )

        # Update doctor profile
        doctor.full_name = data.full_name
        doctor.specialization = data.specialization
        doctor.qualification = data.qualification
        doctor.phone = data.phone
        doctor.email = data.email
        doctor.consultation_fee = data.consultation_fee
        doctor.available_timings = data.available_timings

        # Update login user details also
        if doctor.user_id:
            user = (
                self.db.query(User)
                .filter(User.id == doctor.user_id)
                .first()
            )

            if user:
                user.full_name = data.full_name
                user.email = data.email

                # Only update password if one was supplied
                if getattr(data, "password", None):
                    user.hashed_password = hash_password(data.password)

        self.db.commit()
        self.db.refresh(doctor)

        return doctor