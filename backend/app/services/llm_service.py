from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv
import logging

load_dotenv()

class EmbeddingService:
    def __init__(self):
        try:
            # Using Gemini APIs
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-004")
            self.logger = logging.getLogger(__name__)
            
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY environment variable is required")
        except Exception as e:
            self.logger.error(f"Error getting embedding: {e}")
            raise
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-004",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            self.logger.error(f"Error getting embedding: {e}")
            raise
    
    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts in a batch"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-004",
                input=texts
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            self.logger.error(f"Error getting batch embeddings: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding model"""
        if self.model == "text-embedding-3-small":
            return 1536
        elif self.model == "text-embedding-3-large":
            return 3072
        elif self.model == "text-embedding-ada-002":
            return 1536
        else:
            # Default fallback
            return 1536