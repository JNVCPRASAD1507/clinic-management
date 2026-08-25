from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import require_role
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.report import DashboardResponse

router=APIRouter(prefix="/reports",tags=["Reports"])

@router.get("/dashboard",response_model=DashboardResponse)
def dashboard(db:Session=Depends(get_db),current_user=Depends(require_role("Admin"))):
    today=date.today()
    total_patients=db.query(Patient).count(); total_doctors=db.query(Doctor).count()
    todays=db.query(Appointment).filter(Appointment.appointment_date==today).count()
    upcoming=db.query(Appointment).filter(Appointment.appointment_date>today,Appointment.status!="Cancelled").count()
    completed=db.query(Appointment).filter(Appointment.status=="Completed").count()
    cancelled=db.query(Appointment).filter(Appointment.status=="Cancelled").count()
    most=db.query(Doctor.full_name,func.count(Appointment.id).label("n")).join(Appointment,Appointment.doctor_id==Doctor.id).group_by(Doctor.id,Doctor.full_name).order_by(func.count(Appointment.id).desc()).first()
    first=db.query(func.min(Appointment.appointment_date)).scalar()
    avg=round(db.query(Appointment).count()/((today-first).days+1),2) if first else 0
    return {"total_patients":total_patients,"total_doctors":total_doctors,"todays_appointments":todays,"upcoming_appointments":upcoming,"completed_appointments":completed,"cancelled_appointments":cancelled,"most_visited_doctor":most.full_name if most else None,"average_daily_appointments":avg}

@router.get("/appointments")
def appointment_report(db:Session=Depends(get_db),current_user=Depends(require_role("Admin"))):
    items=db.query(Appointment).all()
    return {"total":len(items),"appointments":items}

@router.get("/doctors")
def doctor_report(db:Session=Depends(get_db),current_user=Depends(require_role("Admin"))):
    return [{"doctor_id":d.id,"doctor_name":d.full_name,"specialization":d.specialization,"total_appointments":db.query(Appointment).filter(Appointment.doctor_id==d.id).count()} for d in db.query(Doctor).all()]
