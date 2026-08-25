# MediFlow+ — Appointment Booking & Clinic Management System

A production-oriented full-stack clinic management assignment using **FastAPI + PostgreSQL + SQLAlchemy + Alembic + JWT + React + Tailwind CSS**.

## Features
- JWT authentication without OAuth2
- RBAC: Admin, Doctor, Receptionist
- Doctor and patient CRUD
- Appointment booking, rescheduling, cancellation and completion/status updates
- Double-booking protection with a database unique constraint and service-level validation
- Prescription creation/update/history
- PDF/JPG/PNG medical report upload, history and download
- BackgroundTasks for appointment confirmation, reminder and prescription notifications
- Search/filter APIs
- Dashboard reports and CSV export
- Audit logs for appointment status changes
- CORS + request middleware
- Swagger/OpenAPI at `/docs`
- Pytest health check
- Docker-ready backend

## Project structure
```text
clinic-management/
├── backend/
│   ├── app/
│   │   ├── core/          # settings, JWT/security
│   │   ├── db/            # SQLAlchemy session
│   │   ├── models/        # database entities
│   │   ├── schemas/       # Pydantic validation
│   │   ├── services/      # background notification logic
│   │   └── routers/       # REST API endpoints
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/components/
│   ├── src/pages/
│   ├── src/context/
│   ├── src/lib/
│   └── package.json
└── postman_collection.json
```

## Database schema
```mermaid
erDiagram
  USERS { int id PK string email string role string }
  DOCTORS { int id PK string email string specialization }
  PATIENTS { int id PK string full_name string phone_number }
  APPOINTMENTS { int id PK string appointment_number int patient_id FK int doctor_id FK date appointment_date time time_slot string status }
  PRESCRIPTIONS { int id PK int appointment_id FK int patient_id FK int doctor_id FK }
  MEDICAL_RECORDS { int id PK int patient_id FK string file_path }
  AUDIT_LOGS { int id PK int appointment_id FK string action }
  PATIENTS ||--o{ APPOINTMENTS : books
  DOCTORS ||--o{ APPOINTMENTS : handles
  APPOINTMENTS ||--o{ PRESCRIPTIONS : creates
  PATIENTS ||--o{ PRESCRIPTIONS : receives
  DOCTORS ||--o{ PRESCRIPTIONS : writes
  PATIENTS ||--o{ MEDICAL_RECORDS : owns
  APPOINTMENTS ||--o{ AUDIT_LOGS : tracks
```

## Backend setup
1. Create PostgreSQL database `clinic_management`.
2. Copy `.env.example` to `.env` and update `DATABASE_URL` and `SECRET_KEY`.
3. Create a virtual environment.
4. Install packages: `pip install -r requirements.txt`.
5. Run migrations after creating a revision: `alembic revision --autogenerate -m "initial schema"` then `alembic upgrade head`.
6. Start API: `uvicorn app.main:app --reload --port 8000`.
7. Open Swagger: `http://localhost:8000/docs`.

The application also calls `Base.metadata.create_all()` at startup for convenient local evaluation. In production, use Alembic as the schema source of truth.

## Frontend setup
```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```
Set `VITE_API_URL` to the deployed backend URL for production. The Axios client automatically adds the JWT bearer token.

## Production deployment
- Backend: deploy the `backend` directory with a PostgreSQL connection string and a strong `SECRET_KEY`.
- Frontend: run `npm run build` and deploy `dist/` to Vercel, Netlify, Firebase Hosting, etc.
- Set frontend `VITE_API_URL=https://your-api-domain.example.com`.
- Set backend `FRONTEND_URL=https://your-frontend-domain.example.com`.
- Run `alembic upgrade head` during deployment.
- Use object storage (S3/GCS/Azure Blob) rather than local `uploads/` for persistent medical documents.
- Replace the demonstration notification function with SMTP/provider credentials before sending real patient email.

## API endpoint coverage
Authentication: `POST /auth/register`, `POST /auth/login`

Doctors: `POST/GET /doctors`, `GET/PUT/DELETE /doctors/{id}`

Patients: `POST/GET /patients`, `GET/PUT/DELETE /patients/{id}`

Appointments: `POST/GET /appointments`, `GET/PUT/DELETE /appointments/{id}`

Prescriptions: `POST/GET /prescriptions`, `GET/PUT /prescriptions/{id}`

Medical records: `POST /medical-records/upload`, `GET /medical-records/{patient_id}`, `GET /medical-records/{patient_id}/download/{record_id}`

Reports: `GET /reports/dashboard`, `GET /reports/appointments`, `GET /reports/doctors`, `GET /reports/appointments/export`

## Important production security notes
- Do not expose unrestricted role selection on public registration; normally an administrator provisions Doctor/Admin accounts.
- Use HTTPS, a strong secret, secure file storage, malware scanning and strict maximum upload sizes.
- For real timed reminders, use a scheduler/queue in addition to `BackgroundTasks`; `BackgroundTasks` is suitable for post-request work but is not a durable job scheduler.
