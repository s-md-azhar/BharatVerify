from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CaseCreate(BaseModel):
    applicant_name: str
    date_of_birth: str
    gender: str
    address: str
    application_id: str
    document_type: str

class CaseResponse(BaseModel):
    id: UUID
    applicant_name: str
    date_of_birth: str
    gender: str
    address: str
    application_id: str
    document_type: str
    status: str
    created_at: datetime
    updated_at: datetime

class RunResponse(BaseModel):
    id: UUID
    case_id: UUID
    status: str
    overall_decision: Optional[str] = None
    latency_ms: Optional[float] = None
    created_at: datetime
