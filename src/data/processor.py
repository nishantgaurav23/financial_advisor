# src/data/processor.py
from pathlib import Path
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from ..utils.config import settings
from .loader import DocumentLoader

class DocumentProcessor:
    """Processes documents into chunks suitable for embedding"""
    
    def __init__(self):
        self.loader = DocumentLoader()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
    
    def process_directory(self, dir_path: Optional[Path] = None) -> List[Document]:
        """Process all documents in a directory"""
        if dir_path is None:
            dir_path = settings.KNOWLEDGE_BASE_DIR
            
        all_documents = []
        
        # Process each file in the directory
        for file_path in self._get_all_files(dir_path):
            documents = self.loader.load_document(file_path)
            if documents:
                all_documents.extend(documents)
        
        # Split documents into chunks
        if all_documents:
            return self.text_splitter.split_documents(all_documents)
        return []
    
    def _get_all_files(self, dir_path: Path) -> List[Path]:
        """Get all supported files in directory and subdirectories"""
        files = []
        for ext in settings.SUPPORTED_EXTENSIONS:
            files.extend(dir_path.rglob(f"*{ext}"))
        return files
