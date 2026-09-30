from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class ExtractedIdentity(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    father_name: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    pin_code: Optional[str] = None
    document_number: Optional[str] = None

class FieldMatchResultBase(BaseModel):
    field: str
    source_value: Optional[str] = None
    application_value: Optional[str] = None
    normalized_source: Optional[str] = None
    normalized_application: Optional[str] = None
    similarity: float = 0.0
    method: str
    decision: str
    confidence: float = 0.0

class FaceMatchResultBase(BaseModel):
    similarity: float = 0.0
    decision: str
    face_found: bool

class VerificationFlagBase(BaseModel):
    flag_type: str
    severity: str
    description: str

class VerificationResultBase(BaseModel):
    case_id: UUID
    run_id: UUID
    overall_status: str
    fields: List[FieldMatchResultBase]
    face_match: Optional[FaceMatchResultBase] = None
    flags: List[VerificationFlagBase] = []
    reasons: List[str] = []
    model_versions: Dict[str, str] = {}
    latency_ms: float
    audit_id: Optional[UUID] = None
    
    model_config = ConfigDict(from_attributes=True)
