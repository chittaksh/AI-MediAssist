from fastapi import APIRouter

from pathlib import Path
from backend.managers.chroma_manager import get_all_documents

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"


router = APIRouter(
    prefix="/chromadb",
    tags=["chromadb"]
)


@router.get("/documents")
def get_chromadb_documents():
    """Retrieve all documents from the ChromaDB collection."""
    return get_all_documents()