# src/data/loader.py
import os
from typing import List, Dict, Optional
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    JSONLoader,
    UnstructuredXMLLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain.schema import Document
from ..utils.config import settings

class DocumentLoader:
    """Handles loading of different document types"""
    
    def __init__(self):
        self.loaders = {
            "pdf": PyPDFLoader,
            "csv": CSVLoader,
            "excel": UnstructuredExcelLoader,
            "json": JSONLoader,
            "xml": UnstructuredXMLLoader,
            "text": TextLoader,
            "markdown": UnstructuredMarkdownLoader
        }
    
    def load_document(self, file_path: Path) -> Optional[List[Document]]:
        """Load a single document"""
        try:
            ext = file_path.suffix.lower()
            if ext not in settings.SUPPORTED_EXTENSIONS:
                print(f"Unsupported file type: {ext}")
                return None
            
            file_type = settings.SUPPORTED_EXTENSIONS[ext]
            loader_class = self.loaders[file_type]
            
            # Special handling for JSON files
            if file_type == "json":
                loader = loader_class(file_path, jq_schema='.[]')
            else:
                loader = loader_class(str(file_path))
            
            print(f"Loading {file_path.name}...")
            return loader.load()
            
        except Exception as e:
            print(f"Error loading {file_path.name}: {str(e)}")
            return None