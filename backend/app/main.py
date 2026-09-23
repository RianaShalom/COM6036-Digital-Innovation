import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Registers the authentication endpoints used for user registration and login.
from app.api.auth import router as auth_router
from app.api.tasks import router as task_router
from app.api.study_sessions import router as study_session_router

app = FastAPI(
    title="StudyBuddy API",
    description="Workload-aware academic task planning API",
    version="0.1.0",
)

# Allows local development and the deployed frontend to access the API.
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    cors_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registers the task management endpoints.
app.include_router(task_router)

# Registers the authentication endpoints.
app.include_router(auth_router)

# Registers the study sessions endpoints.
app.include_router(study_session_router)


# Provides a simple endpoint for checking whether the API is running.
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "StudyBuddy API",
        "version": "0.1.0",
    }