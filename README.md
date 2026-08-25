# CareFlow Clinic Management System

Production-oriented full-stack clinic management system built with:

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** FastAPI + SQLAlchemy + Pydantic
- **Database:** PostgreSQL (SQLite supported for local development)
- **Authentication:** JWT + Argon2 password hashing
- **Migrations:** Alembic
- **Deployment:** Docker + Docker Compose + Nginx

## Project structure

```text
clinic-management-production/
├── backend/
│   ├── app/
│   │   ├── core/              # application configuration
│   │   ├── db/                # SQLAlchemy base/session
│   │   ├── models/            # database models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── repositories/      # database access layer
│   │   ├── services/          # business logic
│   │   └── routers/           # HTTP API endpoints
│   ├── alembic/
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── lib/
│   │   └── pages/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
└── docker-compose.yml
```

## API contract

The frontend is wired directly to these backend endpoints:

| Feature | Endpoint |
|---|---|
| Register | `POST /auth/register` |
| Login | `POST /auth/login` |
| Current user | `GET /auth/me` |
| Patients | `/patients` |
| Doctors | `/doctors` |
| Appointments | `/appointments` |
| Prescriptions | `/prescriptions` |
| Medical records | `/medical-records` |
| Reports | `/reports` |
| Health | `GET /health` |

Swagger documentation is available at `/docs`.

## Local development

### Backend

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

For PostgreSQL, create the database and update `DATABASE_URL` in `.env`.

Run migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

API: `http://localhost:8000`  
Swagger: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend: `http://localhost:5173`

Set `VITE_API_URL=http://localhost:8000` for local development.

## Production with Docker

From the project root:

```bash
docker compose up --build -d
```

Frontend: `http://localhost:5173`  
Backend: `http://localhost:8000`  
Swagger: `http://localhost:8000/docs`

Before exposing this stack publicly:

1. Change `SECRET_KEY`.
2. Change the PostgreSQL password.
3. Set the real frontend origin in `CORS_ORIGINS`.
4. Use HTTPS through your cloud provider or reverse proxy.
5. Put database credentials in deployment secrets, not source control.
6. Use persistent storage for `medical_uploads`.

## Production database migrations

Run:

```bash
docker compose exec backend alembic upgrade head
```

If deploying to a managed PostgreSQL service, point `DATABASE_URL` at the managed database and run the same migration command during deployment.

## Git safety

Do not commit:

- `.env`
- database passwords
- JWT secrets
- uploaded medical records
- `node_modules`
- Python virtual environments

The included `.gitignore` should be extended with deployment-specific secrets if required.

## Important security note

The registration API intentionally keeps the original project's role field so existing API clients remain compatible. For a public production deployment, restrict who can create `Admin` accounts and preferably provision the first administrator through a controlled seed/admin command rather than an open registration form.
