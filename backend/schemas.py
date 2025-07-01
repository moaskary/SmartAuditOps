# backend/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class AuditResultResponse(BaseModel):
    id: int
    timestamp: datetime
    snippet: str
    language: Optional[str]
    results: Dict

    class Config:
        from_attributes = True 