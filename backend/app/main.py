from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.tasks import router as task_router


app = FastAPI(
    title="StudyBuddy API",
    description="Workload-aware academic task planning API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "StudyBuddy API",
        "version": "0.1.0",
    }