from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Tuple
import os
from dotenv import load_dotenv
import logging

from app.models.models import Base, Document, Chunk
from app.models.scheme import DocumentCreate, ChunkCreate

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.logger = logging.getLogger(__name__)
    
    def create_tables(self):
        """Create all tables and enable pgvector extension"""
        try:
            with self.engine.connect() as connection:
                # Enable pgvector extension
                connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                connection.commit()
            
            Base.metadata.create_all(bind=self.engine)
            self.logger.info("Tables created successfully")
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating tables: {e}")
            raise
    
    def get_db(self) -> Session:
        """Get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_document(self, document_data: DocumentCreate) -> Document:
        """Create a new document record"""
        try:
            db_document = Document(
                filename=document_data.filename,
                content_type=document_data.content_type
            )
            self.db.add(db_document)
            self.db.commit()
            self.db.refresh(db_document)
            return db_document
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """Get document by ID"""
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def get_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """Get all documents with pagination"""
        return self.db.query(Document).offset(skip).limit(limit).all()

class ChunkRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_chunk(self, chunk_data: ChunkCreate) -> Chunk:
        """Create a new chunk record"""
        try:
            db_chunk = Chunk(
                document_id=chunk_data.document_id,
                chunk_text=chunk_data.chunk_text,
                chunk_index=chunk_data.chunk_index,
                embedding=chunk_data.embedding
            )
            self.db.add(db_chunk)
            self.db.commit()
            self.db.refresh(db_chunk)
            return db_chunk
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def create_chunks_batch(self, chunks_data: List[ChunkCreate]) -> List[Chunk]:
        """Create multiple chunks in a single transaction"""
        try:
            db_chunks = []
            for chunk_data in chunks_data:
                db_chunk = Chunk(
                    document_id=chunk_data.document_id,
                    chunk_text=chunk_data.chunk_text,
                    chunk_index=chunk_data.chunk_index,
                    embedding=chunk_data.embedding
                )
                db_chunks.append(db_chunk)
            
            self.db.add_all(db_chunks)
            self.db.commit()
            
            for chunk in db_chunks:
                self.db.refresh(chunk)
            
            return db_chunks
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get_chunks_by_document(self, document_id: str) -> List[Chunk]:
        """Get all chunks for a specific document"""
        return self.db.query(Chunk).filter(Chunk.document_id == document_id).all()
    
    def search_similar_chunks(self, query_embedding: List[float], limit: int = 3) -> List[Tuple[Chunk, float]]:
        """Search for similar chunks using cosine similarity"""
        try:
            # Using pgvector's cosine distance operator
            query = text("""
                SELECT c.*, 1 - (c.embedding <=> :query_embedding) as similarity_score
                FROM chunks c
                ORDER BY c.embedding <=> :query_embedding
                LIMIT :limit
            """)
            
            result = self.db.execute(query, {
                'query_embedding': str(query_embedding),
                'limit': limit
            }).fetchall()
            
            chunks_with_scores = []
            for row in result:
                chunk = self.db.query(Chunk).filter(Chunk.id == row[0]).first()
                similarity_score = row[-1]  # Last column is similarity_score
                chunks_with_scores.append((chunk, similarity_score))
            
            return chunks_with_scores
        except SQLAlchemyError as e:
            # Fallback to brute force if pgvector is not available
            return self._brute_force_similarity_search(query_embedding, limit)
    
    def _brute_force_similarity_search(self, query_embedding: List[float], limit: int) -> List[Tuple[Chunk, float]]:
        """Fallback similarity search without pgvector"""
        import numpy as np
        
        all_chunks = self.db.query(Chunk).all()
        similarities = []
        
        for chunk in all_chunks:
            # Calculate cosine similarity
            chunk_embedding = np.array(chunk.embedding)
            query_emb = np.array(query_embedding)
            
            cosine_sim = np.dot(chunk_embedding, query_emb) / (
                np.linalg.norm(chunk_embedding) * np.linalg.norm(query_emb)
            )
            similarities.append((chunk, cosine_sim))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:limit]
    
    def count_chunks_by_document(self, document_id: str) -> int:
        """Count chunks for a specific document"""
        return self.db.query(Chunk).filter(Chunk.document_id == document_id).count()