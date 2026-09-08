from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="StudyBuddy API",                         # Identifies the API in the documentation
    description="Workload-aware academic task planning API",
    version="0.1.0",                               # Tracks the current API version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],       # Allows requests from the frontend during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",                       # Confirms that the API is running correctly
        "service": "StudyBuddy API",
        "version": "0.1.0",
    }