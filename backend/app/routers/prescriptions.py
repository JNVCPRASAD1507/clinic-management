from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import Appointment, Prescription, User, UserRole, Doctor
from app.schemas.common import PrescriptionCreate, PrescriptionOut, PrescriptionUpdate
from app.core.security import require_roles, get_current_user
from app.services.notifications import prescription_notification
router=APIRouter(prefix="/prescriptions",tags=["Prescriptions"])
@router.post("",response_model=PrescriptionOut)
def create(data:PrescriptionCreate,background_tasks:BackgroundTasks,db:Session=Depends(get_db),user:User=Depends(require_roles(UserRole.DOCTOR))):
    a=db.get(Appointment,data.appointment_id)
    if not a:raise HTTPException(404,"Appointment not found")
    if a.doctor.email!=user.email:raise HTTPException(403,"Not assigned to this appointment")
    obj=Prescription(patient_id=a.patient_id,doctor_id=a.doctor_id,**data.model_dump());db.add(obj);db.commit();db.refresh(obj)
    prescription_notification(background_tasks,f"patient-{a.patient.phone_number}@example.com",obj.id)
    return obj
@router.get("",response_model=list[PrescriptionOut])
def list_prescriptions(patient_id:int|None=None,db:Session=Depends(get_db),_:User=Depends(get_current_user)):
    q=db.query(Prescription)
    if patient_id:q=q.filter(Prescription.patient_id==patient_id)
    return q.order_by(Prescription.created_at.desc()).all()
@router.get("/{id}",response_model=PrescriptionOut)
def get(id:int,db:Session=Depends(get_db),_:User=Depends(get_current_user)):
    obj=db.get(Prescription,id)
    if not obj:raise HTTPException(404,"Prescription not found")
    return obj
@router.put("/{id}",response_model=PrescriptionOut)
def update(id:int,data:PrescriptionUpdate,db:Session=Depends(get_db),user:User=Depends(require_roles(UserRole.DOCTOR))):
    obj=db.get(Prescription,id)
    if not obj:raise HTTPException(404,"Prescription not found")
    doctor=db.query(Doctor).filter(Doctor.id==obj.doctor_id,Doctor.email==user.email).first()
    if not doctor: raise HTTPException(403,"Not allowed to update this prescription")
    for k,v in data.model_dump(exclude_unset=True).items():setattr(obj,k,v)
    db.commit();db.refresh(obj);return obj
