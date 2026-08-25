from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import Patient, UserRole
from app.schemas.common import PatientCreate, PatientOut, PatientUpdate
from app.core.security import require_roles, get_current_user
router=APIRouter(prefix="/patients",tags=["Patients"])
@router.post("",response_model=PatientOut)
def create(data:PatientCreate,db:Session=Depends(get_db),_:object=Depends(require_roles(UserRole.ADMIN,UserRole.RECEPTIONIST))):
    obj=Patient(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj
@router.get("",response_model=list[PatientOut])
def list_patients(search:str|None=None,db:Session=Depends(get_db),_:object=Depends(get_current_user)):
    q=db.query(Patient)
    if search:q=q.filter(Patient.full_name.ilike(f"%{search}%"))
    return q.order_by(Patient.full_name).all()
@router.get("/{id}",response_model=PatientOut)
def get(id:int,db:Session=Depends(get_db),_:object=Depends(get_current_user)):
    obj=db.get(Patient,id)
    if not obj:raise HTTPException(404,"Patient not found")
    return obj
@router.put("/{id}",response_model=PatientOut)
def update(id:int,data:PatientUpdate,db:Session=Depends(get_db),_:object=Depends(require_roles(UserRole.ADMIN,UserRole.RECEPTIONIST))):
    obj=db.get(Patient,id)
    if not obj:raise HTTPException(404,"Patient not found")
    for k,v in data.model_dump().items():setattr(obj,k,v)
    db.commit();db.refresh(obj);return obj
@router.delete("/{id}")
def delete(id:int,db:Session=Depends(get_db),_:object=Depends(require_roles(UserRole.ADMIN))):
    obj=db.get(Patient,id)
    if not obj:raise HTTPException(404,"Patient not found")
    db.delete(obj);db.commit();return {"message":"Patient removed"}
