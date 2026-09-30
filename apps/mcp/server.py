from mcp.server.mcpserver import MCPServer
import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Create an MCP server
mcp = MCPServer("BharatVerify")

@mcp.tool()
def extract_document_text(image_path: str) -> str:
    """Extracts text from an identity document image using PaddleOCR."""
    from services.ocr.paddle_ocr import get_ocr_service
    ocr = get_ocr_service()
    return ocr.extract_text(image_path)

@mcp.tool()
def extract_identity_fields(raw_text: str) -> dict:
    """Extracts structured identity fields from raw OCR text using LLM."""
    from services.ocr.extraction import extract_identity_fields as run_extraction
    return run_extraction(raw_text)

@mcp.tool()
def verify_faces(selfie_path: str, document_path: str) -> dict:
    """Compares a selfie with a document photo to verify identity."""
    from services.face.face_verification import get_face_service
    face_svc = get_face_service()
    return face_svc.verify_faces(selfie_path, document_path)

if __name__ == "__main__":
    mcp.run()
