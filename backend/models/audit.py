
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, Dict
from datetime import datetime

from ..database import Base

class AuditResult(Base):
    __tablename__ = "audit_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    snippet: Mapped[str] = mapped_column(String)
    language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    results: Mapped[Dict] = mapped_column(JSON)