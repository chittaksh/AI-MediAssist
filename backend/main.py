"""FastAPI service that exposes the saved arrival-delay model."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from backend.managers.chroma_manager import search_collection
from backend.RAG.rag_chain import rag_search
from backend.managers.auth_manager import create_table
from backend.routers import chroma, files, users



class QueryRequest(BaseModel):
    input: str

create_table()

@asynccontextmanager
async def lifespan(_: FastAPI):
    """Load the trusted local model once when the API starts."""
    global model, model_metadata

    # if not DATA_DIR.is_dir():
    #     raise RuntimeError(
    #         f"Data storage directory not found at {DATA_DIR}"
    #     )
    # if not METRICS_PATH.is_file():
    #     raise RuntimeError(
    #         f"Model metadata not found at {METRICS_PATH}. Run `python train.py` first."
    #     )

    # 1. Setup code runs on application startup
    # await database.connect()
    
    try:
        # 2. Yield control back to Starlette/FastAPI
        yield 
    finally:
        # 3. Shutdown code runs when the server stops
        # await database.disconnect()
        pass


app = FastAPI(
    title="MediAssist AI API",
    description="API for the MediAssist AI Capstone Project, insights based on uploaded files.",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(users.router)
app.include_router(files.router)
app.include_router(chroma.router)


@app.get("/health")
def health() -> dict[str, object]:
    """Report service readiness."""
    return {
        "status": "ok"
    }


@app.post("/query")
def query_model(query_request: QueryRequest):
    """Accept a query and return the model's response."""
    # Placeholder implementation - replace with actual model inference logic
    return {"response": rag_search.invoke({"query": query_request.input})}


@app.post("/search-documents")
def search_documents(query_request: QueryRequest):
    """Retrieve documents from the ChromaDB collection based on a search query."""
    return search_collection(query_request.input)