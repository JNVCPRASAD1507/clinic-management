from fastapi import FastAPI

from fastapi import FastAPI

from app.routers import (
    auth,
    doctors,
    patients,
    appointments,
    prescriptions,
    medical_records,
    reports
)

app = FastAPI(
    title="Appointment Booking & Clinic Management System",
    description="Backend API for clinic management and appointment booking",
    version="1.0.0",
    docs_url="/"
)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "success",
        "message": "Appointment Booking & Clinic Management System is running"
    }


app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(prescriptions.router)
app.include_router(medical_records.router)
app.include_router(reports.router)