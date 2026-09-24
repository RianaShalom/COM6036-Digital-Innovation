# StudyBuddy

**Workload aware academic task planning for students**

StudyBuddy is a distributed web application designed to help students manage academic tasks by considering more than just deadlines. It combines deadline urgency, estimated effort, task difficulty, and current workload to produce an explainable priority score for each outstanding task.

The application was developed as the **COM6036 Digital Innovation** coursework.

## Live Application

**Frontend:**
https://studybuddy-nine-pied.vercel.app/

**Backend API:**
Hosted on Render.

**API health endpoint:**
`/api/health`

The production deployment uses Vercel for the React frontend, Render for the FastAPI backend, and Render PostgreSQL for persistent data storage.

> The current PostgreSQL deployment uses Render's free plan and is scheduled to expire on **23 October 2026** unless the database plan is upgraded.

The FastAPI backend provides REST endpoints for authentication, tasks, prioritisation, and study sessions.

---

## Features

### Account management

* User registration
* Secure password hashing using Argon2
* JWT-based authentication
* Protected API endpoints
* User-specific data isolation

### Academic task management

Users can:

* Create academic tasks
* Specify the module
* Set a deadline
* Estimate required study hours
* Set task difficulty from 1–5
* Add an optional description
* View outstanding tasks
* Update tasks
* Delete tasks
* Mark tasks as complete

### Workload-aware priority engine

StudyBuddy calculates an explainable priority score using:

* Deadline urgency
* Estimated effort
* Task difficulty
* Current workload pressure

The current weighting is:

```text
Priority =
    45% Urgency
  + 25% Effort
  + 20% Difficulty
  + 10% Workload Pressure
```

Each component is normalised to a 0–100 scale.

Priority levels are then assigned as:

|    Score | Level    |
| -------: | -------- |
|   80–100 | Critical |
| 60–79.99 | High     |
| 40–59.99 | Medium   |
|  0–39.99 | Low      |

The dashboard displays the individual factors contributing to each priority score so that users can understand why a task has been prioritised.

### Workload pressure

Workload pressure considers outstanding estimated study hours relative to the time available before a task's deadline.

The prototype uses a configurable assumption of **4 study hours per available day**.

This is a heuristic rather than an empirically validated measurement. The system does not claim to determine an objectively optimal study schedule.

### Study session tracking

Users can record study time against their tasks.

StudyBuddy provides:

* Study session recording
* Duration validation
* Task ownership validation
* Total recorded study time
* Total study time in hours

### Dashboard

The dashboard provides:

* Number of outstanding tasks
* Estimated outstanding workload
* Critical task count
* High-priority task count
* Medium-priority task count
* Low-priority task count
* Prioritised task list
* Priority explanations
* Task completion controls

---

## Architecture

```text
                         Internet
                            |
                            v
                  +--------------------+
                  |      Vercel        |
                  | React + TypeScript |
                  |   Presentation     |
                  +--------------------+
                            |
                     HTTPS / REST / JSON
                            |
                            v
                  +--------------------+
                  |      Render        |
                  |     FastAPI        |
                  |   Business Logic   |
                  +--------------------+
                            |
                         SQLAlchemy
                            |
                            v
                  +--------------------+
                  | Render PostgreSQL  |
                  |    Data Layer      |
                  +--------------------+
```

---

## Technology Stack

| Area                 | Technology        |
| -------------------- | ----------------- |
| Frontend             | React             |
| Frontend language    | TypeScript        |
| Frontend build tool  | Vite              |
| Frontend HTTP client | Axios             |
| Backend              | FastAPI           |
| Backend language     | Python            |
| ORM                  | SQLAlchemy        |
| Validation           | Pydantic          |
| Database             | PostgreSQL        |
| Authentication       | JWT               |
| Password hashing     | Argon2            |
| Testing              | pytest + HTTPX    |
| Frontend hosting     | Vercel            |
| Backend hosting      | Render            |
| Database hosting     | Render PostgreSQL |
| Source control       | Git / GitHub      |

---

### Authentication

```text
POST /api/auth/register
POST /api/auth/login
```

Authentication uses JWT access tokens.

### Tasks

The API supports operations for:

```text
GET    /api/tasks
GET    /api/tasks/prioritized
POST   /api/tasks
PUT    /api/tasks/{task_id}
DELETE /api/tasks/{task_id}
POST   /api/tasks/{task_id}/complete
```

### Study sessions

```text
POST /api/study-sessions
GET  /api/study-sessions/summary
```

The API also provides automatically generated OpenAPI documentation through FastAPI.

---

## Security

StudyBuddy includes several security controls appropriate for the prototype:

* Passwords are hashed rather than stored as plaintext.
* Argon2 is used for password hashing.
* JWTs are used for authenticated API access.
* Protected endpoints require authentication.
* Users can only modify their own tasks.
* Study sessions can only be recorded against tasks owned by the authenticated user.
* Database relationships use foreign keys.
* Production communication uses HTTPS.
* Production secrets are supplied through environment variables rather than committed to Git.

The local `.env` file is excluded from version control.

---

## Configuration

### Backend

The backend requires environment variables such as:

```text
DATABASE_URL
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
FRONTEND_URL
```

Local configuration:

```text
DATABASE_URL=<local PostgreSQL connection string>
SECRET_KEY=<development secret>
ACCESS_TOKEN_EXPIRE_MINUTES=60
FRONTEND_URL=http://localhost:5173
```

Production values are configured through Render environment variables and are not stored in the repository.

### Frontend

The frontend uses:

```text
VITE_API_URL
```

For local development this points to the local FastAPI server.

For production it points to the deployed Render API.

---

## Running Locally

### Backend

From the `backend` directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure the required environment variables, then initialise the database:

```bash
python -m app.db.init_db
```

Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

Set `VITE_API_URL` in the frontend environment configuration to point to the local FastAPI server.

---

## Testing

The backend includes automated tests using **pytest** and **HTTPX**.

Tests cover areas including:

* User registration
* Authentication
* Protected endpoints
* Task creation
* Task updates
* Task deletion
* Task completion
* Task ownership
* Priority calculation
* Workload-aware prioritisation
* Study session creation
* Study session validation
* Study session ownership
* Study session summaries

Run the backend test suite from the `backend` directory:

```bash
pytest
```

The frontend production build can be checked with:

```bash
npm run build
```

---

## Deployment

StudyBuddy is deployed as a distributed application.

### Frontend

The React application is deployed using **Vercel**.

The frontend deployment is configured with:

```text
Root Directory: frontend
Framework: Vite
Build Command: npm run build
Output Directory: dist
```

### Backend

The FastAPI application is deployed using **Render**.

The backend uses:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
```

The service starts using:

```bash
python -m app.db.init_db && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Database

The production PostgreSQL database is hosted by Render.

The backend connects to it using the `DATABASE_URL` environment variable.

### CORS

The backend allows local development origins and the deployed Vercel frontend through the `FRONTEND_URL` environment variable.

This allows the same FastAPI application to support both local development and the production frontend without hard-coding the production domain.

---

## Deployment Verification

The deployed system has been tested end-to-end.

The production verification included:

1. Loading the React application from Vercel.
2. Registering a user account.
3. Signing in successfully.
4. Creating an academic task.
5. Persisting the task through the FastAPI API.
6. Retrieving the task from PostgreSQL.
7. Calculating workload-aware priority.
8. Displaying the priority factors in the React dashboard.

---

## Future Development

Potential future improvements include:

* Learning typical task completion times from historical study sessions.
* Allowing users to configure daily study capacity.
* Incorporating assessment weighting.
* Adding recurring academic tasks.
* Providing calendar integration.
* Adding historical workload analytics.
* Improving accessibility and keyboard navigation.
* Introducing database migrations using Alembic.
* Adding more comprehensive frontend automated testing.

These features are outside the current prototype scope.

---

## Project Context

StudyBuddy was developed as an individual **Level 6 Digital Innovation** project.

The application demonstrates:

* A real-world academic productivity problem
* Requirements-driven development
* N-tier architecture
* Distributed deployment
* RESTful API design
* Secure authentication
* Relational data modelling
* Explainable workload-aware prioritisation
* Automated backend testing
* Cloud deployment
* Critical consideration of system limitations
