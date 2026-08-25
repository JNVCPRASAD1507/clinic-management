import csv, io
from datetime import date, timedelta
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import Appointment, AppointmentStatus, Doctor, Patient, User, UserRole
from app.core.security import require_roles
router=APIRouter(prefix="/reports",tags=["Reports"])
@router.get("/dashboard")
def dashboard(db:Session=Depends(get_db),_:User=Depends(require_roles(UserRole.ADMIN))):
    today=date.today(); total=db.query(Appointment).count()
    completed=db.query(Appointment).filter(Appointment.status==AppointmentStatus.COMPLETED).count()
    cancelled=db.query(Appointment).filter(Appointment.status==AppointmentStatus.CANCELLED).count()
    most=db.query(Doctor.full_name,func.count(Appointment.id).label("visits")).join(Appointment).group_by(Doctor.id).order_by(func.count(Appointment.id).desc()).first()
    return {"total_patients":db.query(Patient).count(),"total_doctors":db.query(Doctor).count(),"todays_appointments":db.query(Appointment).filter(Appointment.appointment_date==today).count(),"upcoming_appointments":db.query(Appointment).filter(Appointment.appointment_date>today,Appointment.status.notin_([AppointmentStatus.CANCELLED,AppointmentStatus.COMPLETED])).count(),"completed_appointments":completed,"cancelled_appointments":cancelled,"most_visited_doctor":most[0] if most else None,"average_daily_appointments":round(total/max((today-date(2026,1,1)).days,1),2)}
@router.get("/appointments")
def appointment_report(db:Session=Depends(get_db),_:User=Depends(require_roles(UserRole.ADMIN))):
    return db.query(Appointment).order_by(Appointment.appointment_date.desc()).all()
@router.get("/doctors")
def doctor_report(db:Session=Depends(get_db),_:User=Depends(require_roles(UserRole.ADMIN))):
    return db.query(Doctor.full_name,Doctor.specialization,func.count(Appointment.id).label("appointments")).outerjoin(Appointment).group_by(Doctor.id).order_by(func.count(Appointment.id).desc()).all()
@router.get("/appointments/export")
def export_csv(db:Session=Depends(get_db),_:User=Depends(require_roles(UserRole.ADMIN))):
    output=io.StringIO();w=csv.writer(output);w.writerow(["Appointment Number","Patient","Doctor","Date","Time","Status"])
    for a in db.query(Appointment).all():w.writerow([a.appointment_number,a.patient.full_name,a.doctor.full_name,a.appointment_date,a.time_slot,a.status.value])
    output.seek(0);return StreamingResponse(iter([output.getvalue()]),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=appointments.csv"})
