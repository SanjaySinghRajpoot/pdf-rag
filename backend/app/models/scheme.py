from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class DocumentCreate(BaseModel):
    filename: str
    content_type: str

class DocumentResponse(BaseModel):
    id: uuid.UUID
    filename: str
    content_type: str
    upload_timestamp: datetime
    chunks_count: int
    
    class Config:
        from_attributes = True

class ChunkCreate(BaseModel):
    document_id: uuid.UUID
    chunk_text: str
    chunk_index: int
    embedding: List[float]

class ChunkResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    chunk_text: str
    chunk_index: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Query string for semantic search")
    limit: int = Field(default=3, ge=1, le=10, description="Number of results to return")

class QueryResult(BaseModel):
    chunk_text: str
    similarity_score: float
    document_id: uuid.UUID
    chunk_index: int

class QueryResponse(BaseModel):
    query: str
    results: List[QueryResult]
    processing_time: float

class IngestResponse(BaseModel):
    document_id: uuid.UUID
    filename: str
    chunks_processed: int
    processing_time: float
    message: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None