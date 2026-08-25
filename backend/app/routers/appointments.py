from datetime import date
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import Appointment, AppointmentStatus, AuditLog, Doctor, Patient, User, UserRole
from app.schemas.common import AppointmentCreate, AppointmentOut, AppointmentUpdate
from app.core.security import get_current_user, require_roles
from app.services.notifications import appointment_confirmation, appointment_reminder
router=APIRouter(prefix="/appointments",tags=["Appointments"])

def serialize(a):
    return {"id":a.id,"appointment_number":a.appointment_number,"patient_id":a.patient_id,"doctor_id":a.doctor_id,"appointment_date":a.appointment_date,"time_slot":a.time_slot,"reason_for_visit":a.reason_for_visit,"status":a.status,"patient_name":a.patient.full_name if a.patient else None,"doctor_name":a.doctor.full_name if a.doctor else None}

@router.post("",response_model=AppointmentOut)
def create(data:AppointmentCreate,background_tasks:BackgroundTasks,db:Session=Depends(get_db),_:User=Depends(require_roles(UserRole.ADMIN,UserRole.RECEPTIONIST))):
    if not db.get(Patient,data.patient_id) or not db.get(Doctor,data.doctor_id): raise HTTPException(404,"Patient or doctor not found")
    obj=Appointment(appointment_number=f"APT-{uuid4().hex[:8].upper()}",**data.model_dump())
    db.add(obj)
    try: db.commit()
    except IntegrityError: db.rollback(); raise HTTPException(409,"Doctor already has this time slot")
    db.refresh(obj)
    patient=db.get(Patient,obj.patient_id); doctor=db.get(Doctor,obj.doctor_id)
    appointment_confirmation(background_tasks, f"patient-{patient.phone_number}@example.com", obj.appointment_number)
    appointment_reminder(background_tasks, f"patient-{patient.phone_number}@example.com", obj.appointment_number)
    return serialize(obj)

@router.get("",response_model=list[AppointmentOut])
def list_appointments(patient_name:str|None=None,doctor_name:str|None=None,appointment_number:str|None=None,status:AppointmentStatus|None=None,appointment_date:date|None=None,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    q=db.query(Appointment).join(Patient).join(Doctor)
    if user.role==UserRole.DOCTOR:
        q=q.filter(Doctor.email==user.email)
    if patient_name:q=q.filter(Patient.full_name.ilike(f"%{patient_name}%"))
    if doctor_name:q=q.filter(Doctor.full_name.ilike(f"%{doctor_name}%"))
    if appointment_number:q=q.filter(Appointment.appointment_number.ilike(f"%{appointment_number}%"))
    if status:q=q.filter(Appointment.status==status)
    if appointment_date:q=q.filter(Appointment.appointment_date==appointment_date)
    return [serialize(x) for x in q.order_by(Appointment.appointment_date,Appointment.time_slot).all()]

@router.get("/{id}",response_model=AppointmentOut)
def get(id:int,db:Session=Depends(get_db),_:User=Depends(get_current_user)):
    obj=db.get(Appointment,id)
    if not obj:raise HTTPException(404,"Appointment not found")
    return serialize(obj)

@router.put("/{id}",response_model=AppointmentOut)
def update(id:int,data:AppointmentUpdate,db:Session=Depends(get_db),user:User=Depends(require_roles(UserRole.ADMIN,UserRole.RECEPTIONIST,UserRole.DOCTOR))):
    obj=db.get(Appointment,id)
    if not obj:raise HTTPException(404,"Appointment not found")
    if user.role==UserRole.DOCTOR and obj.doctor.email!=user.email:raise HTTPException(403,"Not assigned to this appointment")
    old=obj.status.value
    changes=data.model_dump(exclude_unset=True)
    for k,v in changes.items():setattr(obj,k,v)
    if any(k in changes for k in ("doctor_id","appointment_date","time_slot")):
        conflict=db.query(Appointment).filter(Appointment.doctor_id==obj.doctor_id,Appointment.appointment_date==obj.appointment_date,Appointment.time_slot==obj.time_slot,Appointment.id!=obj.id,Appointment.status.notin_([AppointmentStatus.CANCELLED])).first()
        if conflict:raise HTTPException(409,"Doctor already has this time slot")
    if obj.status.value!=old:db.add(AuditLog(appointment_id=obj.id,action="status_update",old_status=old,new_status=obj.status.value))
    db.commit();db.refresh(obj);return serialize(obj)

@router.delete("/{id}")
def delete(id:int,db:Session=Depends(get_db),_:User=Depends(require_roles(UserRole.ADMIN,UserRole.RECEPTIONIST))):
    obj=db.get(Appointment,id)
    if not obj:raise HTTPException(404,"Appointment not found")
    obj.status=AppointmentStatus.CANCELLED;db.commit();return {"message":"Appointment cancelled"}
