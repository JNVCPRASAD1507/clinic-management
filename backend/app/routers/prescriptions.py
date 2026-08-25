from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import require_role
from app.models.appointment import Appointment
from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse
from app.services.notification_service import send_prescription_notification
from app.services.prescription_service import PrescriptionService

router=APIRouter(prefix="/prescriptions",tags=["Prescriptions"])

@router.post("",response_model=PrescriptionResponse,status_code=201)
def create_prescription(data:PrescriptionCreate,background_tasks:BackgroundTasks,db:Session=Depends(get_db),current_user=Depends(require_role("Doctor"))):
    p=PrescriptionService(db).create(data)
    phone=db.query(__import__("app.models.patient",fromlist=["Patient"]).Patient.phone).filter(__import__("app.models.patient",fromlist=["Patient"]).Patient.id==p.patient_id).scalar()
    if phone: background_tasks.add_task(send_prescription_notification,phone,p.id)
    return p

@router.get("",response_model=list[PrescriptionResponse])
def get_prescriptions(db:Session=Depends(get_db),current_user=Depends(require_role("Admin","Doctor"))): return db.query(Prescription).order_by(Prescription.id.desc()).all()

@router.get("/{prescription_id}",response_model=PrescriptionResponse)
def get_prescription(prescription_id:int,db:Session=Depends(get_db),current_user=Depends(require_role("Admin","Doctor"))):
    p=db.query(Prescription).filter(Prescription.id==prescription_id).first()
    if not p: raise HTTPException(404,"Prescription not found")
    return p

@router.put("/{prescription_id}",response_model=PrescriptionResponse)
def update_prescription(prescription_id:int,data:PrescriptionCreate,db:Session=Depends(get_db),current_user=Depends(require_role("Doctor"))):
    p=db.query(Prescription).filter(Prescription.id==prescription_id).first()
    if not p: raise HTTPException(404,"Prescription not found")
    for k,v in data.model_dump(exclude={"appointment_id"},exclude_unset=True).items(): setattr(p,k,v)
    db.commit(); db.refresh(p); return p
