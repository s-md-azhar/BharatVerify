# Architectural & Implementation Decisions

1. **Monorepo Structure**: Placed both React frontend and FastAPI backend in one repository for ease of development and testing in a portfolio context.
2. **PostgreSQL**: Selected for robust relational data storage and JSONB support for varying extracted fields and model metadata.
3. **PaddleOCR**: Chosen for strong multilingual support (specifically Hindi/Marathi/Devanagari) and lightweight mobile models suited for a 6GB VRAM environment.
4. **BGE-M3 Embeddings**: BAAI/bge-m3 is excellent for cross-lingual tasks (English, Hindi, Marathi) and semantic similarity.
5. **PyTorch Classifier over pure LLM**: An LLM is not ideal or deterministic enough for precise, multi-signal identity matching. We train a PyTorch MLP on deterministic and semantic signals.
6. **LangGraph for Agent Orchestration**: LangGraph provides explicit state management, perfect for the stateful, step-by-step nature of a verification pipeline.
7. **YuNet + SFace**: Lightweight, ONNX-compatible models for face detection and recognition, avoiding heavy dependencies like deepface.
8. **Server-Sent Events (SSE)**: Chosen over WebSockets for simpler unidirectional real-time progress updates to the frontend.
9. **Environment Constraints (8GB RAM, 6GB VRAM)**: Models will be loaded lazily. The embedding model and face models can fall back to CPU to prevent CUDA OOM errors.
