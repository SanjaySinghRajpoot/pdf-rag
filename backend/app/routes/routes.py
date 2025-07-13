from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.services.db_interaction import DatabaseManager
from sqlalchemy.orm import Session
from typing import List

from app.controller.controller import DocumentController, HealthController
from app.models.scheme import QueryRequest, QueryResponse, IngestResponse, ErrorResponse

# Initialize database manager
db_manager = DatabaseManager()

# Create API router
api_router = APIRouter()

# Dependency to get database session
def get_db():
    return next(db_manager.get_db())

@api_router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Ingest a document (PDF or TXT file) into the system.
    
    - Accepts PDF or TXT files
    - Chunks the text into ~500-word segments
    - Generates embeddings for each chunk
    - Stores chunks and embeddings in the database
    """
    controller = DocumentController(db)
    return await controller.ingest_document(file)

@api_router.post("/query", response_model=QueryResponse)
def query_documents(
    query_request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Query documents using semantic search.
    
    - Accepts a query string
    - Generates embedding for the query
    - Performs nearest-neighbor search
    - Returns top-k most similar text chunks
    """
    controller = DocumentController(db)
    return controller.query_documents(query_request)

@api_router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    
    - Checks database connectivity
    - Returns system status
    """
    controller = HealthController(db)
    return controller.health_check()

@api_router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Get system statistics.
    
    - Returns document and chunk counts
    - Provides system insights
    """
    controller = HealthController(db)
    return controller.get_stats()