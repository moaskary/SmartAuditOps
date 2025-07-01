from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import database, models, schemas


# Import our AI analysis function
from huggingface_tasks.classify_text import analyze_code_snippet

# Create a router to group our audit endpoints
router = APIRouter(
    prefix="/audit",
    tags=["Audit"] # This will group our endpoints in the API docs
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally: 
        db.close()

# Define the request data model using Pydantic
class CodeSnippet(BaseModel):
    snippet: str
    language: str | None = None # Optional language field

@router.get("/", response_model=List[schemas.AuditResultResponse])
def get_all_audits(db: Session = Depends(get_db)):
    """
    Retrieves all audit results from the database.
    """
    audits = db.query(models.audit.AuditResult).order_by(models.audit.AuditResult.timestamp.desc()).all()
    return audits

@router.post("/code")
def audit_code_snippet(payload: CodeSnippet, db: Session = Depends(get_db)):
    """
    Receives a code snippet, performs an AI analysis, and saves the result.
    """
    analysis_result = analyze_code_snippet(payload.snippet)

    # --- THIS IS THE CORRECTED BLOCK ---
    db_audit = models.audit.AuditResult(
        snippet=payload.snippet,
        language=payload.language,
        results=analysis_result # <--- THE FIX IS HERE (results, with an 's')
    )
    
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    
    return db_audit