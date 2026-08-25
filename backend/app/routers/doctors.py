from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import Doctor, UserRole
from app.schemas.common import DoctorCreate, DoctorOut, DoctorUpdate
from app.core.security import require_roles, get_current_user
router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("", response_model=DoctorOut)
def create(data: DoctorCreate, db: Session = Depends(get_db), _: object = Depends(require_roles(UserRole.ADMIN))):
    if db.query(Doctor).filter(Doctor.email == data.email).first(): raise HTTPException(409, "Doctor email already exists")
    obj=Doctor(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj
@router.get("", response_model=list[DoctorOut])
def list_doctors(search: str | None = None, specialization: str | None = None, db: Session = Depends(get_db), _: object = Depends(get_current_user)):
    q=db.query(Doctor)
    if search: q=q.filter(Doctor.full_name.ilike(f"%{search}%"))
    if specialization: q=q.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    return q.order_by(Doctor.full_name).all()
@router.get("/{id}", response_model=DoctorOut)
def get(id:int, db:Session=Depends(get_db), _:object=Depends(get_current_user)):
    obj=db.get(Doctor,id)
    if not obj: raise HTTPException(404,"Doctor not found")
    return obj
@router.put("/{id}", response_model=DoctorOut)
def update(id:int,data:DoctorUpdate,db:Session=Depends(get_db),_:object=Depends(require_roles(UserRole.ADMIN))):
    obj=db.get(Doctor,id)
    if not obj: raise HTTPException(404,"Doctor not found")
    for k,v in data.model_dump().items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj
@router.delete("/{id}")
def delete(id:int,db:Session=Depends(get_db),_:object=Depends(require_roles(UserRole.ADMIN))):
    obj=db.get(Doctor,id)
    if not obj: raise HTTPException(404,"Doctor not found")
    db.delete(obj); db.commit(); return {"message":"Doctor removed"}
