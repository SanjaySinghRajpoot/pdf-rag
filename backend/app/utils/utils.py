import PyPDF2
from typing import List, BinaryIO
import os
from dotenv import load_dotenv
import logging

load_dotenv()

class TextProcessor:
    def __init__(self):
        self.chunk_size = int(os.getenv("CHUNK_SIZE", 500))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 50))
        self.logger = logging.getLogger(__name__)
    
    def extract_text_from_pdf(self, file: BinaryIO) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {e}")
            raise
    
    def extract_text_from_txt(self, file: BinaryIO) -> str:
        """Extract text from TXT file"""
        try:
            content = file.read()
            if isinstance(content, bytes):
                return content.decode('utf-8').strip()
            return content.strip()
        except Exception as e:
            self.logger.error(f"Error extracting text from TXT: {e}")
            raise
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        if not text:
            return []
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk = " ".join(chunk_words)
            chunks.append(chunk)
            
            # Break if we've reached the end
            if i + self.chunk_size >= len(words):
                break
        
        return chunks
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        return '\n'.join(lines)

class FileValidator:
    def __init__(self):
        self.max_file_size = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB
        self.allowed_extensions = {'.pdf', '.txt'}
        self.allowed_content_types = {
            'application/pdf',
            'text/plain',
            'text/txt'
        }
    
    def validate_file(self, filename: str, content_type: str, file_size: int) -> bool:
        """Validate file based on extension, content type, and size"""
        # Check file size
        if file_size > self.max_file_size:
            raise ValueError(f"File size exceeds maximum limit of {self.max_file_size} bytes")
        
        # Check file extension
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension not in self.allowed_extensions:
            raise ValueError(f"File type not supported. Allowed types: {self.allowed_extensions}")
        
        # Check content type
        if content_type not in self.allowed_content_types:
            raise ValueError(f"Content type not supported. Allowed types: {self.allowed_content_types}")
        
        return True
    
    def get_file_extension(self, filename: str) -> str:
        """Get file extension"""
        return os.path.splitext(filename)[1].lower()

class ResponseFormatter:
    @staticmethod
    def format_error_response(error: str, detail: str = None) -> dict:
        """Format error response"""
        response = {"error": error}
        if detail:
            response["detail"] = detail
        return response
    
    @staticmethod
    def format_success_response(data: dict, message: str = "Success") -> dict:
        """Format success response"""
        response = {"message": message}
        response.update(data)
        return response