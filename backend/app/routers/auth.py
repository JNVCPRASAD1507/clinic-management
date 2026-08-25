from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import User
from app.schemas.common import LoginRequest, TokenResponse, UserRegister
from app.core.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, "Email already registered")
    user = User(full_name=data.full_name, email=data.email, password_hash=hash_password(data.password), role=data.role)
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_access_token(user), "token_type": "bearer", "user": {"id": user.id, "full_name": user.full_name, "email": user.email, "role": user.role.value}}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_access_token(user), "token_type": "bearer", "user": {"id": user.id, "full_name": user.full_name, "email": user.email, "role": user.role.value}}
