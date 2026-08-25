from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from time import perf_counter


class RequestLoggingMiddleware(BaseHTTPMiddleware):
# // This is middleware. It runs for every HTTP request that comes into your FastAPI application.
# //the middleware measures how long the request takes. Suppose it takes 0.0352 seconds.    
    async def dispatch(self, request, call_next):
        started = perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{perf_counter()-started:.4f}"
        return response


from app.core.config import settings
from app.db.session import Base, engine
from app.routers import (
    auth,
    doctors,
    patients,
    appointments,
    prescriptions,
    records,
    reports,
)
import app.models

app = FastAPI(
    title="Clinic Management API",
    version="1.0.0",
    description="Appointment booking and clinic management backend",
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(prescriptions.router)
app.include_router(records.router)
app.include_router(reports.router)


# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)    
# "When FastAPI starts, execute Base.metadata.create_all(engine)."

# create_all() tells SQLAlchemy to create the tables represented by your Base.metadata
# if they don't already exist. SQLAlchemy checks for existing tables before creating them by default

@app.get("/")
def root():
    return {
        "message": "Clinic Management API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok"}
