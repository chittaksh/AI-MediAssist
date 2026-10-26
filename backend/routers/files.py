from fastapi import APIRouter, HTTPException, HTTPException, UploadFile, File

import os
import shutil
from pathlib import Path

from backend.RAG.ingestion import ingest_documents
from backend.managers.chroma_manager import delete_by_filename

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

# 3. Create the folder if it doesn't exist
RAW_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(
    prefix="/files",
    tags=["files"]
)


@router.get("/list", response_model=list[str])
def get_file_list():
    """Return a list of all files in the data directory."""
    return [f.name for f in RAW_DIR.iterdir() if f.is_file()]


@router.post("/upload", response_model=dict[str, str])
async def file_upload(file: UploadFile = File(...)):
    """Accepts a file upload and saves it to the server."""
    # Create the complete file destination path safely
    file_path = os.path.join(RAW_DIR, file.filename)
    
    # Save the file using standard stream copying
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_documents(file.filename)  # Call the ingestion function to process the uploaded file
        
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_path": file_path
    }


@router.delete("/delete/{file_name}")
def delete_file(file_name: str):
    """Delete a file from the data directory."""
    file_path = RAW_DIR / file_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        file_path.unlink()  # Delete the file
        delete_by_filename(file_name)  # Delete associated entries in ChromaDB
        return {"detail": f"File {file_name} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

