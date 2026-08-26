from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import (
    auth,
    doctors,
    patients,
    appointments,
    prescriptions,
    medical_records,
    reports,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-ready clinic appointment and records API",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    return {"name": settings.app_name, "version": settings.app_version, "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "success", "message": "Clinic Management System API is running"}


app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(prescriptions.router)
app.include_router(medical_records.router)
app.include_router(reports.router)
