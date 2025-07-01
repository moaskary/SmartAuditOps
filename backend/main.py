from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 1. IMPORT the middleware
from backend.routes import audit

from . import database
from .models import audit as audit_model

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="SmartAuditOps API",
    description="API for AI-powered code, security, and compliance reviews.",
    version="0.1.0"
)

# 2. DEFINE the frontend URLs that are allowed to connect
origins = [
    "http://localhost:5173",  # The address of your React dev server
    "http://localhost",
]

# 3. ADD the middleware to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies which origins are allowed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(audit.router)

@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "SmartAuditOps Backend is running!"}