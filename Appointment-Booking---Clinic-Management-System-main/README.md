# Appointment Booking & Clinic Management System

A backend application for managing clinic operations including user authentication, doctors, patients, appointments, prescriptions, medical records, background notifications, audit logging, and reports.

## Project Objective

The Appointment Booking & Clinic Management System provides REST APIs that allow a clinic to manage its day-to-day operations through a secure FastAPI backend.

The system supports:

- User Authentication
- JWT Authentication
- Role-Based Authorization
- Doctor Management
- Patient Management
- Appointment Scheduling
- Prescription Management
- Medical Records
- Background Tasks
- Search and Filtering
- Pagination and Sorting
- Audit Logs
- Reports Dashboard

---

# User Roles

## Admin

- Manage doctors
- Manage patients
- View all appointments
- View reports

## Doctor

- View assigned appointments
- Update appointment status
- Create prescriptions
- Update prescriptions
- View patient medical history

## Receptionist

- Register patients
- Schedule appointments
- Reschedule appointments
- Cancel appointments

---

# Doctor Management

Supported operations:

- Create doctor
- View all doctors
- View doctor details
- Update doctor
- Delete doctor

Doctor fields:

- Full Name
- Specialization
- Qualification
- Phone Number
- Email
- Consultation Fee
- Available Timings

---

# Patient Management

Supported operations:

- Register patient
- View patients
- View patient details
- Update patient
- Delete patient

Patient fields:

- Full Name
- Age
- Gender
- Phone Number
- Address
- Blood Group
- Emergency Contact

---

# Appointment Management

Supported operations:

- Book appointment
- View appointments
- View appointment details
- Reschedule appointment
- Update appointment status
- Cancel appointment
- Complete appointment

Appointment fields:

- Appointment Number
- Patient
- Doctor
- Appointment Date
- Time Slot
- Reason for Visit
- Status

Appointment statuses:

- Scheduled
- Confirmed
- Completed
- Cancelled
- No Show

## Double Booking Prevention

The system checks whether a doctor is already booked for the requested date and time slot. If the slot is already occupied, the appointment is rejected.

---

# Search and Filtering

Appointments support filtering by:

- Patient Name
- Doctor Name
- Appointment Number
- Appointment Status
- Appointment Date
- Specialization

Example:

```text
GET /appointments?patient_name=Rahul
```

---

# Pagination and Sorting

Appointment listing supports pagination and sorting.

Supported parameters:

- `page`
- `page_size`
- `sort_by`
- `sort_order`

Example:

```text
GET /appointments?page=1&page_size=5&sort_by=appointment_date&sort_order=asc
```

---

# Prescription Management

Doctors can:

- Create prescriptions
- View prescriptions
- View prescription details
- Update prescriptions

A prescription can only be created for a completed appointment.

Prescription fields:

- Diagnosis
- Medicines
- Dosage
- Instructions
- Follow-up Date

---

# Medical Records

The system supports:

- Upload medical reports
- View patient medical history
- Download medical reports

Supported file types:

- PDF
- JPG
- PNG

---

# Background Tasks

FastAPI `BackgroundTasks` are used for:

- Appointment confirmation
- Appointment reminder
- Prescription notification

The current notification service demonstrates the notification process through server-side output.

---

# Audit Logs

Audit logging is implemented for appointment-related operations such as:

- Appointment update
- Appointment status change
- Appointment cancellation

Audit information includes:

- User ID
- Appointment ID
- Action
- Description
- Created timestamp

---

# Reports

## Dashboard

```text
GET /reports/dashboard
```

Provides:

- Total Patients
- Total Doctors
- Today's Appointments
- Upcoming Appointments
- Completed Appointments
- Cancelled Appointments
- Most Visited Doctor
- Average Daily Appointments

## Appointment Report

```text
GET /reports/appointments
```

## Doctor Report

```text
GET /reports/doctors
```

---

# API Endpoints

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Login and generate JWT |

## Doctors

| Method | Endpoint | Description |
|---|---|---|
| POST | `/doctors` | Create doctor |
| GET | `/doctors` | Get doctors |
| GET | `/doctors/{doctor_id}` | Get doctor details |
| PUT | `/doctors/{doctor_id}` | Update doctor |
| DELETE | `/doctors/{doctor_id}` | Delete doctor |

## Patients

| Method | Endpoint | Description |
|---|---|---|
| POST | `/patients` | Register patient |
| GET | `/patients` | Get patients |
| GET | `/patients/{patient_id}` | Get patient details |
| PUT | `/patients/{patient_id}` | Update patient |
| DELETE | `/patients/{patient_id}` | Delete patient |

## Appointments

| Method | Endpoint | Description |
|---|---|---|
| POST | `/appointments` | Book appointment |
| GET | `/appointments` | Get appointments |
| GET | `/appointments/{appointment_id}` | Get appointment |
| PUT | `/appointments/{appointment_id}` | Update/reschedule appointment |
| DELETE | `/appointments/{appointment_id}` | Cancel appointment |

## Prescriptions

| Method | Endpoint | Description |
|---|---|---|
| POST | `/prescriptions` | Create prescription |
| GET | `/prescriptions` | Get prescriptions |
| GET | `/prescriptions/{prescription_id}` | Get prescription |
| PUT | `/prescriptions/{prescription_id}` | Update prescription |

## Medical Records

| Method | Endpoint | Description |
|---|---|---|
| POST | `/medical-records/upload` | Upload medical report |
| GET | `/medical-records/{patient_id}` | View patient records |

## Reports

| Method | Endpoint | Description |
|---|---|---|
| GET | `/reports/dashboard` | Dashboard report |
| GET | `/reports/appointments` | Appointment report |
| GET | `/reports/doctors` | Doctor report |

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Backend framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pydantic | Data validation |
| JWT | Authentication |
| Alembic | Database migrations |
| Uvicorn | ASGI server |
| FastAPI BackgroundTasks | Background processing |
| Swagger / OpenAPI | API documentation |

---

# Database Design

PostgreSQL is used as the primary database.

SQLAlchemy is used for ORM-based database operations and relationships.

Alembic is used to manage database migrations.

Main entities:

- Users
- Doctors
- Patients
- Appointments
- Prescriptions
- Medical Records
- Audit Logs

The database schema diagram is included as:

```text
Database Schema Diagram.png
```

---

# Project Structure

```text
Appointment Booking & Clinic Management System/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   ├── dependencies.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   └── services/
│
├── alembic/
│   └── versions/
│
├── uploads/
├── Screenshots/
│
├── Database Schema Diagram.png
├── appointment_clinic_management_postman_collection.json
├── requirements.txt
├── alembic.ini
├── .env
└── README.md
```

---

# Installation and Setup

## Prerequisites

- Python
- PostgreSQL
- Git

## 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

## 2. Navigate to the Project

```bash
cd "Appointment Booking & Clinic Management System"
```

## 3. Create Virtual Environment

```powershell
python -m venv .venv
```

## 4. Activate Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

## 5. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

If required by the environment:

```powershell
python -m pip install email-validator argon2-cffi
```

## 6. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/clinic_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Do not commit `.env` to GitHub.

## 7. Run Database Migrations

```powershell
python -m alembic upgrade head
```

## 8. Start the Application

```powershell
python -m uvicorn app.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

---

# Swagger / OpenAPI Documentation

Swagger UI:

```text
http://127.0.0.1:8000/
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

Swagger can be used to:

- View endpoints
- View request schemas
- View response schemas
- Authenticate using JWT
- Execute API requests
- Test protected endpoints

---

# Authentication Flow

## Register

```text
POST /auth/register
```

Example:

```json
{
  "full_name": "Nayana SM",
  "email": "nayanasm@gmail.com",
  "password": "Nayana@123",
  "role": "Receptionist"
}
```

## Login

```text
POST /auth/login
```

Example:

```json
{
  "email": "admin2@gmail.com",
  "password": "Admin@123"
}
```

The login response provides a JWT access token.

Use it for protected APIs:

```text
Authorization: Bearer <access_token>
```

---

# Postman Collection

The Postman collection is included in the project:

```text
appointment_clinic_management_postman_collection.json
```

It contains requests for:

- Authentication
- Doctors
- Patients
- Appointments
- Prescriptions
- Medical Records
- Reports

Import the JSON file into Postman.

Recommended testing flow:

1. Register user
2. Login
3. Copy the access token
4. Save the token in the collection variable
5. Test protected endpoints

---

# Testing

The APIs were tested using:

- Swagger UI
- Postman

Testing covered:

- User registration
- User login
- JWT authentication
- Role-based authorization
- Doctor management
- Patient management
- Appointment management
- Double booking prevention
- Appointment search and filtering
- Pagination
- Sorting
- Prescription management
- Medical records
- Background task notifications
- Reports dashboard
- Appointment reports
- Doctor reports
- Audit logging

---

# Error Handling

The API uses appropriate HTTP status codes:

- `200 OK`
- `201 Created`
- `400 Bad Request`
- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`
- `422 Unprocessable Entity`

Handled cases include:

- Invalid credentials
- Unauthorized role access
- Doctor not found
- Patient not found
- Appointment not found
- Duplicate appointment booking
- Duplicate prescription
- Invalid request data
- Invalid medical record file type

---

# Security

Security features include:

- JWT authentication
- Password hashing
- Role-Based Access Control
- Protected endpoints
- Pydantic validation
- Environment variables for sensitive configuration
- Medical record file validation
- Doctor-specific appointment authorization

---

# Bonus Features

## Implemented

- Double booking prevention
- Pagination
- Sorting
- Audit logs

## Not Implemented

- CSV export
- Docker support
- Pytest test suite

Docker and Pytest are optional/bonus enhancements.

---

# Deliverables

The project includes:

- Source Code
- README Documentation
- Swagger / OpenAPI Documentation
- Database Schema Diagram
- Postman Collection
- Swagger Screenshots

---

# Screenshots

Swagger testing screenshots are stored in:

```text
Screenshots/
```

They demonstrate API requests and successful responses for the implemented modules.

---

# Code Quality

The project follows a modular backend architecture with separate:

- Models
- Schemas
- Routers
- Authentication
- Dependencies
- Services
- Database configuration

SQLAlchemy is used for database access and relationships.

Pydantic is used for request and response validation.

---

# Future Enhancements

Possible future improvements:

- CSV appointment export
- Docker containerization
- Automated email integration
- SMS notifications
- Pytest test suite
- Advanced analytics
- Scheduled appointment reminders
- Cloud storage for medical records

---

# Author

**Nayana SM**

Backend Engineering Assignment

**Appointment Booking & Clinic Management System**
