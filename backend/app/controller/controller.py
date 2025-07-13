from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List
import time
import logging
import uuid

from app.services.db_interaction import DocumentRepository, ChunkRepository
from app.services.llm_service import EmbeddingService
from app.utils.utils import TextProcessor, FileValidator
from app.models.scheme import (
    DocumentCreate, ChunkCreate, QueryRequest, 
    QueryResponse, IngestResponse, QueryResult
)

class DocumentController:
    def __init__(self, db: Session):
        self.db = db
        self.document_repo = DocumentRepository(db)
        self.chunk_repo = ChunkRepository(db)
        self.embedding_service = EmbeddingService()
        self.text_processor = TextProcessor()
        self.file_validator = FileValidator()
        self.logger = logging.getLogger(__name__)
    
    async def ingest_document(self, file: UploadFile) -> IngestResponse:
        """Process and ingest a document"""
        start_time = time.time()
        
        try:
            # Validate file
            file_content = await file.read()
            file_size = len(file_content)
            
            self.file_validator.validate_file(
                filename=file.filename,
                content_type=file.content_type,
                file_size=file_size
            )
            
            # Extract text based on file type
            file_extension = self.file_validator.get_file_extension(file.filename)
            
            if file_extension == '.pdf':
                from io import BytesIO
                text = self.text_processor.extract_text_from_pdf(BytesIO(file_content))
            elif file_extension == '.txt':
                from io import BytesIO
                text = self.text_processor.extract_text_from_txt(BytesIO(file_content))
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")
            
            # Clean and chunk text
            cleaned_text = self.text_processor.clean_text(text)
            chunks = self.text_processor.chunk_text(cleaned_text)
            
            if not chunks:
                raise HTTPException(status_code=400, detail="No text content found in file")
            
            # Create document record
            document_data = DocumentCreate(
                filename=file.filename,
                content_type=file.content_type
            )
            document = self.document_repo.create_document(document_data)
            
            # Generate embeddings for all chunks
            embeddings = self.embedding_service.get_embeddings_batch(chunks)
            
            # Create chunk records
            chunk_data_list = []
            for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_data = ChunkCreate(
                    document_id=document.id,
                    chunk_text=chunk_text,
                    chunk_index=i,
                    embedding=embedding
                )
                chunk_data_list.append(chunk_data)
            
            # Save chunks to database
            self.chunk_repo.create_chunks_batch(chunk_data_list)
            
            processing_time = time.time() - start_time
            
            return IngestResponse(
                document_id=document.id,
                filename=file.filename,
                chunks_processed=len(chunks),
                processing_time=processing_time,
                message="Document ingested successfully"
            )
            
        except Exception as e:
            self.logger.error(f"Error ingesting document: {e}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=str(e))
    
    def query_documents(self, query_request: QueryRequest) -> QueryResponse:
        """Query documents using semantic search"""
        start_time = time.time()
        
        try:
            # Generate embedding for query
            query_embedding = self.embedding_service.get_embedding(query_request.query)
            
            # Search for similar chunks
            similar_chunks = self.chunk_repo.search_similar_chunks(
                query_embedding=query_embedding,
                limit=query_request.limit
            )
            
            # Format results
            results = []
            for chunk, similarity_score in similar_chunks:
                result = QueryResult(
                    chunk_text=chunk.chunk_text,
                    similarity_score=similarity_score,
                    document_id=chunk.document_id,
                    chunk_index=chunk.chunk_index
                )
                results.append(result)
            
            processing_time = time.time() - start_time
            
            return QueryResponse(
                query=query_request.query,
                results=results,
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Error querying documents: {e}")
            raise HTTPException(status_code=500, detail=str(e))

class HealthController:
    def __init__(self, db: Session):
        self.db = db
        self.document_repo = DocumentRepository(db)
        self.chunk_repo = ChunkRepository(db)
    
    def health_check(self) -> dict:
        """Basic health check"""
        try:
            # Test database connection
            documents_count = len(self.document_repo.get_documents(limit=1))
            return {
                "status": "healthy",
                "database": "connected",
                "documents_in_db": documents_count
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
    
    def get_stats(self) -> dict:
        """Get system statistics"""
        try:
            documents = self.document_repo.get_documents(limit=1000) 
            total_documents = len(documents)
            
            total_chunks = 0
            for doc in documents:
                total_chunks += self.chunk_repo.count_chunks_by_document(str(doc.id))
            
            return {
                "total_documents": total_documents,
                "total_chunks": total_chunks,
                "average_chunks_per_document": total_chunks / total_documents if total_documents > 0 else 0
            }
        except Exception as e:
            return {
                "error": str(e)
            }