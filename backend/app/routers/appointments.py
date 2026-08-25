from datetime import date
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import require_role
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.services.appointment_service import AppointmentService
from app.services.notification_service import send_appointment_confirmation, send_appointment_reminder

router=APIRouter(prefix="/appointments",tags=["Appointments"])

@router.post("",response_model=AppointmentResponse,status_code=201)
def create_appointment(data:AppointmentCreate,background_tasks:BackgroundTasks,db:Session=Depends(get_db),current_user=Depends(require_role("Admin","Receptionist"))):
    a=AppointmentService(db).create(data)
    phone=db.query(Patient.phone).filter(Patient.id==a.patient_id).scalar()
    if phone:
        background_tasks.add_task(send_appointment_confirmation,phone,a.appointment_number)
        background_tasks.add_task(send_appointment_reminder,phone,a.appointment_number)
    return a

@router.get("",response_model=list[AppointmentResponse])
def get_appointments(patient_name:str|None=None,doctor_name:str|None=None,appointment_number:str|None=None,appointment_status:str|None=None,appointment_date:date|None=None,specialization:str|None=None,page:int=1,page_size:int=10,sort_by:str="appointment_date",sort_order:str="asc",db:Session=Depends(get_db),current_user=Depends(require_role("Admin","Doctor","Receptionist"))):
    if page<1: raise HTTPException(400,"Page must be greater than or equal to 1")
    if not 1<=page_size<=100: raise HTTPException(400,"Page size must be between 1 and 100")
    fields={"id":Appointment.id,"appointment_date":Appointment.appointment_date,"appointment_number":Appointment.appointment_number,"status":Appointment.status,"time_slot":Appointment.time_slot}
    if sort_by not in fields: raise HTTPException(400,"Invalid sort_by")
    if sort_order.lower() not in {"asc","desc"}: raise HTTPException(400,"sort_order must be 'asc' or 'desc'")
    q=db.query(Appointment).join(Patient,Appointment.patient_id==Patient.id).join(Doctor,Appointment.doctor_id==Doctor.id)
    if current_user.role=="Doctor":
        doctor=db.query(Doctor).filter(Doctor.user_id==current_user.id).first()
        if not doctor: raise HTTPException(404,"Doctor profile not found")
        q=q.filter(Appointment.doctor_id==doctor.id)
    if patient_name: q=q.filter(Patient.full_name.ilike(f"%{patient_name}%"))
    if doctor_name: q=q.filter(Doctor.full_name.ilike(f"%{doctor_name}%"))
    if appointment_number: q=q.filter(Appointment.appointment_number.ilike(f"%{appointment_number}%"))
    if appointment_status: q=q.filter(Appointment.status==appointment_status)
    if appointment_date: q=q.filter(Appointment.appointment_date==appointment_date)
    if specialization: q=q.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    col=fields[sort_by]; q=q.order_by(col.desc() if sort_order.lower()=="desc" else col.asc())
    return q.offset((page-1)*page_size).limit(page_size).all()

@router.get("/{appointment_id}",response_model=AppointmentResponse)
def get_appointment(appointment_id:int,db:Session=Depends(get_db),current_user=Depends(require_role("Admin","Doctor","Receptionist"))):
    a=db.query(Appointment).filter(Appointment.id==appointment_id).first()
    if not a: raise HTTPException(404,"Appointment not found")
    if current_user.role=="Doctor":
        d=db.query(Doctor).filter(Doctor.id==a.doctor_id).first()
        if not d or d.user_id!=current_user.id: raise HTTPException(403,"Not authorized to view this appointment")
    return a

@router.put("/{appointment_id}",response_model=AppointmentResponse)
def update_appointment(appointment_id:int,data:AppointmentUpdate,db:Session=Depends(get_db),current_user=Depends(require_role("Admin","Receptionist","Doctor"))):
    return AppointmentService(db).update(appointment_id,data,current_user.id,current_user.role)

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id:int,db:Session=Depends(get_db),current_user=Depends(require_role("Admin","Receptionist"))):
    AppointmentService(db).cancel(appointment_id,current_user.id)
    return {"message":"Appointment cancelled successfully"}
