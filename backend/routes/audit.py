
from fastapi import APIRouter, Body
from pydantic import BaseModel

# Import our AI analysis function
from huggingface_tasks.classify_text import analyze_code_snippet

# Create a router to group our audit endpoints
router = APIRouter(
    prefix="/audit",
    tags=["Audit"] # This will group our endpoints in the API docs
)

# Define the request data model using Pydantic
class CodeSnippet(BaseModel):
    snippet: str
    language: str | None = None # Optional language field

@router.post("/code")
def audit_code_snippet(payload: CodeSnippet):
    """
    Receives a code snippet and returns an AI-powered analysis.
    """
    analysis_result = analyze_code_snippet(payload.snippet)
    return {"file_name": "example.py", "results": analysis_result}