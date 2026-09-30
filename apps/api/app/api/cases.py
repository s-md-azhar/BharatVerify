import json
import asyncio
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import os

from app.core.database import get_db
from app.schemas.cases import CaseCreate, CaseResponse, RunResponse
from app.models.domain import VerificationCase, Document, VerificationRun
from services.agent.workflow import verification_agent, VerificationState

router = APIRouter()

@router.post("/", response_model=CaseResponse)
def create_case(case_in: CaseCreate, db: Session = Depends(get_db)):
    db_case = VerificationCase(**case_in.model_dump())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

@router.get("/", response_model=List[CaseResponse])
def get_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cases = db.query(VerificationCase).offset(skip).limit(limit).all()
    return cases

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: UUID, db: Session = Depends(get_db)):
    case = db.query(VerificationCase).filter(VerificationCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.post("/{case_id}/documents")
def upload_document(case_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    case = db.query(VerificationCase).filter(VerificationCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", f"{case_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        
    doc = Document(case_id=case.id, filename=file.filename, file_path=file_path, document_type=case.document_type)
    db.add(doc)
    db.commit()
    return {"message": "Document uploaded successfully", "filename": file.filename}

@router.get("/{case_id}/verify/stream")
async def start_verification_stream(case_id: UUID, db: Session = Depends(get_db)):
    case = db.query(VerificationCase).filter(VerificationCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    doc = db.query(Document).filter(Document.case_id == case_id).first()
    if not doc:
        raise HTTPException(status_code=400, detail="No document uploaded")
        
    run = VerificationRun(case_id=case.id, status="STARTED")
    db.add(run)
    db.commit()
    db.refresh(run)

    async def event_generator():
        initial_state = VerificationState(
            case_id=str(case.id),
            run_id=str(run.id),
            applicant_data={
                "name": case.applicant_name,
                "date_of_birth": case.date_of_birth,
                "gender": case.gender,
                "address": case.address,
                "document_type": case.document_type,
                "pin": "" # Assuming simple for now
            },
            document_path=doc.file_path,
            selfie_path=None,
            ocr_raw_text=None,
            extracted_identity=None,
            match_results=None,
            face_result=None,
            flags=[],
            agent_traces=[],
            overall_status=None,
            errors=[]
        )
        
        yield f"data: {json.dumps({'status': 'STARTED'})}\n\n"
        await asyncio.sleep(0.1)
        
        # LangGraph Stream execution
        try:
            for s in verification_agent.stream(initial_state):
                # The state after each node execution
                # 's' is a dict mapping node_name -> state_update
                node_name = list(s.keys())[0]
                update = s[node_name]
                yield f"data: {json.dumps({'status': f'COMPLETED_{node_name.upper()}', 'traces': update.get('agent_traces', [])})}\n\n"
                await asyncio.sleep(0.1)
                
                if node_name == "decision":
                    final_status = update.get("overall_status", "ERROR")
                    yield f"data: {json.dumps({'status': 'FINISHED', 'decision': final_status})}\n\n"
                    # We should save results to DB here in production
        except Exception as e:
            yield f"data: {json.dumps({'status': 'ERROR', 'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
