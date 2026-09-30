from sqlalchemy import Column, String, ForeignKey, JSON, Float, Boolean, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class DemoOperator(BaseModel):
    __tablename__ = "demo_operators"
    
    username = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)

class VerificationCase(BaseModel):
    __tablename__ = "verification_cases"
    
    operator_id = Column(ForeignKey("demo_operators.id"), nullable=True)
    applicant_name = Column(String(200))
    date_of_birth = Column(String(50))
    gender = Column(String(20))
    address = Column(Text)
    application_id = Column(String(100), unique=True, index=True)
    document_type = Column(String(50))
    status = Column(String(50), default="PENDING")
    
    runs = relationship("VerificationRun", back_populates="case")

class Document(BaseModel):
    __tablename__ = "documents"
    
    case_id = Column(ForeignKey("verification_cases.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    document_type = Column(String(50))
    mime_type = Column(String(50))

class VerificationRun(BaseModel):
    __tablename__ = "verification_runs"
    
    case_id = Column(ForeignKey("verification_cases.id"), nullable=False)
    status = Column(String(50))
    overall_decision = Column(String(50))
    latency_ms = Column(Float)
    
    case = relationship("VerificationCase", back_populates="runs")
    audit_events = relationship("AuditEvent", back_populates="run")

class ExtractedField(BaseModel):
    __tablename__ = "extracted_fields"
    
    run_id = Column(ForeignKey("verification_runs.id"), nullable=False)
    field_name = Column(String(100))
    raw_value = Column(Text)
    normalized_value = Column(Text)
    confidence = Column(Float)
    extraction_method = Column(String(50))

class FieldMatchResult(BaseModel):
    __tablename__ = "field_match_results"
    
    run_id = Column(ForeignKey("verification_runs.id"), nullable=False)
    field_name = Column(String(100))
    source_value = Column(Text)
    application_value = Column(Text)
    similarity_score = Column(Float)
    match_method = Column(String(100))
    decision = Column(String(50))

class FaceMatchResult(BaseModel):
    __tablename__ = "face_match_results"
    
    run_id = Column(ForeignKey("verification_runs.id"), nullable=False)
    similarity_score = Column(Float)
    decision = Column(String(50))
    face_found = Column(Boolean, default=False)

class VerificationFlag(BaseModel):
    __tablename__ = "verification_flags"
    
    run_id = Column(ForeignKey("verification_runs.id"), nullable=False)
    flag_type = Column(String(100))
    severity = Column(String(50))
    description = Column(Text)

class AuditEvent(BaseModel):
    __tablename__ = "audit_events"
    
    run_id = Column(ForeignKey("verification_runs.id"), nullable=False)
    event_type = Column(String(100), nullable=False)
    component = Column(String(100))
    status = Column(String(50))
    latency_ms = Column(Float)
    metadata_json = Column(JSON, nullable=True)
    
    run = relationship("VerificationRun", back_populates="audit_events")

class ModelVersion(BaseModel):
    __tablename__ = "model_versions"
    
    component = Column(String(100), nullable=False)
    version = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

class EvaluationRun(BaseModel):
    __tablename__ = "evaluation_runs"
    
    model_version_id = Column(ForeignKey("model_versions.id"), nullable=True)
    dataset_name = Column(String(100))
    metrics_json = Column(JSON)
