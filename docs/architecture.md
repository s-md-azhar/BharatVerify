# BharatVerify Architecture

## High-Level Architecture

BharatVerify uses a modular architecture combining a modern React frontend, a FastAPI backend, and an orchestrated LangGraph agent that coordinates various ML and deterministic services.

```mermaid
graph TD
    UI[React UI (TypeScript + Tailwind)] -->|REST / SSE| API[FastAPI API Gateway]
    
    API --> Agent[Agent Service (LangGraph)]
    API --> Audit[Audit Service]
    API --> Verification[Verification Service]
    API --> DB[(PostgreSQL)]
    
    Agent --> OCR[OCR Service (PaddleOCR)]
    Agent --> Match[Matching Service]
    Agent --> Face[Face Verification (YuNet + SFace)]
    
    Match --> Embed[Embedding Model (BGE-M3)]
    Match --> PyTorch[PyTorch Classifier]
    Match --> FAISS[(FAISS Index)]
```

## Core Components

1. **Frontend (React + Vite + Tailwind)**: Enterprise compliance operations UI.
2. **Backend (FastAPI)**: REST endpoints and SSE for real-time verification updates.
3. **Database (PostgreSQL)**: Stores cases, runs, audit events, features, and model metadata.
4. **Agent Orchestration (LangGraph)**: Manages the pipeline workflow dynamically to route ambiguous cases.
5. **Machine Learning Pipeline**:
   - **OCR**: PaddleOCR (English, Hindi, Marathi).
   - **Embeddings**: BAAI/bge-m3.
   - **Face Verification**: YuNet + SFace.
   - **Identity Matcher**: Custom-trained PyTorch MLP for identity resolution.
6. **MCP Server**: Exposes safe internal capabilities for advanced integrations.

## Data Flow
- Case is created via API.
- Synthetic document is uploaded.
- Agent starts the extraction pipeline (OCR).
- Extracted fields are normalized.
- Fuzzy matching, embeddings, and PyTorch classifier score the identity matches.
- Rules engine dictates VERIFIED, REVIEW, or MISMATCH.
- All actions are logged into the Audit Service.
