# BharatVerify

A realistic, production-oriented AI-powered KYC/identity verification platform inspired by enterprise compliance operations.

## What It Demonstrates
- Python and clean software engineering
- Git/GitHub and PR-quality workflows
- PyTorch and actual model training
- ML fundamentals and rigorous evaluation
- REST APIs and FastAPI
- Transformer fundamentals
- LLM APIs and prompting (Gemini 3.8 Flash)
- Function/tool calling & Structured outputs (JSON Schema)
- Embeddings and semantic similarity (BGE-M3)
- Agent loops (LangGraph)
- Model serving & evaluation
- React, TypeScript, and enterprise UX design

## Architecture
(See `docs/architecture.md`)

## Demo
(Placeholder for Demo Link/Screenshots)

## Pipeline
Document → OCR → Normalization → Matching → Face Verification → Decision → Audit

## ML Methodology
(See `docs/ml-pipeline.md`)

## Evaluation
(Placeholder for actual evaluation results)

## Error Analysis
(Placeholder for actual failure categories)

## Agent Architecture
(See `docs/agent-architecture.md`)

## MCP
(See `docs/mcp.md`)

## Security
(See `docs/security.md`)

## Local Setup
```bash
# Clone
git clone https://github.com/s-md-azhar/BharatVerify.git
cd BharatVerify

# Environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
cd apps/api
uvicorn app.main:app --reload

# Frontend
cd apps/web
npm install
npm run dev
```

## Docker
```bash
docker-compose up --build
```

## Limitations
Synthetic benchmark results do not represent production KYC accuracy. The platform uses synthetic data and is for demonstration purposes only.

## Future Work
- More comprehensive RAG implementations.
- Expanded document support.
