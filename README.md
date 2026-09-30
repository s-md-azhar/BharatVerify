# BharatVerify - AI-Powered KYC Platform
## Portfolio-Grade Prototype / Synthetic KYC Demonstration

### Purpose
BharatVerify is a realistic, production-oriented AI-powered KYC/identity verification platform inspired by the public product/workflow positioning of modern KYC platforms. It is built strictly as a portfolio project to demonstrate capabilities across end-to-end full stack machine learning and software engineering.

## Architecture
- **Frontend**: React, Tailwind CSS (Vite), emphasizing a professional, enterprise compliance operations console without excessive "AI" styling.
- **Backend API**: FastAPI, providing RESTful endpoints with OpenAPI generation.
- **Database**: PostgreSQL (via Docker Compose) handling stateful records and agent paths.
- **Agent Orchestration**: LangGraph, defining a stateful graph (Extract -> Match -> Review/RAG -> Face -> Decision) with conditional edges.
- **Models**:
  - LLM: Google Gemini (via `google-genai` SDK) for structured extraction (Pydantic schema) and tool calling.
  - Embedding: `BAAI/bge-m3` configured as the primary model, with graceful fallback to `paraphrase-multilingual-MiniLM-L12-v2` for environments with constrained RAM (<=8GB).
  - Neural Matcher: PyTorch MLP (10 -> 64 -> 64 -> 1) trained on synthetic text embeddings and fuzzy features.
  - RAG: FAISS + Embeddings for policy retrieval and review augmentation.

## End-to-End Workflow
1. **Extraction (Gemini)**: Extracts Name, DOB, Address, Gender from OCR text.
2. **Matching (PyTorch MLP)**: Compares extracted fields against application fields using token features and embeddings.
3. **Review (RAG FAISS)**: If match is ambiguous, queries the FAISS vector database for policy rules.
4. **Face Verification**: Validates identity visually (simulated with OpenCV).
5. **Decision**: Final outcome generated based on rules, thresholds, and ML scores.

## Evaluation & Metrics
The model was trained on a hard synthetic dataset designed with:
- Strict disjoint splits (0% identity overlap between train/val/test) to prevent data leakage.
- Intentional OCR artifacts, Typos, and Devanagari transliteration edge cases.

### Model Comparison
A comparative benchmark was executed on 900 held-out test pairs comparing different approaches to identity matching under realistic OCR noise conditions:

- **Exact Match Baseline**: F1 59.3%, FPR 26.8%, FNR 46.4%. High precision but fails dramatically on OCR noise.
- **Fuzzy Matcher**: F1 88.3%, FPR 13.7%, FNR 10.0%. Very high recall but suffers false positives on similar names.
- **PyTorch MLP Matcher**: F1 97.3%, FPR 1.5%, FNR 3.7%. (A fully trained model integrating class weights, optimal dimensionality, embeddings, and fuzzy features to achieve superior non-linear combination. This benchmark was generated using the local constrained training fallback embedder: `paraphrase-multilingual-MiniLM-L12-v2`).

Results demonstrate the capability of combining embeddings and fuzzy features, ready for further dataset augmentation and tuning.

## Setup Instructions
1. `docker compose up -d` (requires Docker Desktop running)
2. `pip install -r requirements.txt`
3. Set `GEMINI_API_KEY` and `DATABASE_URL` in `.env`.
4. Run `python scripts/run_migrations.py`
5. Run `uvicorn apps.api.app.main:app --reload`

## Deployment Architecture

### Frontend (Vercel)
Built using React + Vite. It communicates with the backend via `VITE_API_BASE_URL`. Do NOT expose API keys in the frontend bundle.

### Backend (Render)
Built with FastAPI. 
Deploy to Render using a Web Service configured via `render.yaml`. 
Ensure you define:
- `GEMINI_API_KEY`
- `DATABASE_URL`
- `ENVIRONMENT=production`
- `EMBEDDING_MODEL=bge-m3` (Fallback to `paraphrase-multilingual-MiniLM-L12-v2` ONLY for low-VRAM local dev).
- `FRONTEND_URL` (for CORS).

File Storage is treated as ephemeral metadata parsing. No persistent buckets are used; the database strictly holds extracted application claims and paths.
