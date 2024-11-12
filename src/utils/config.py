# src/utils/config.py
from pathlib import Path
from typing import Dict, Any
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    KNOWLEDGE_BASE_DIR: Path = BASE_DIR / "data" / "knowledge_base"
    EMBEDDINGS_DIR: Path = BASE_DIR / "data" / "embeddings"
    
    # Model settings
    EMBEDDING_MODEL: str = "BAAI/bge-small-en"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # File types supported
    SUPPORTED_EXTENSIONS: Dict[str, str] = {
        ".pdf": "pdf",
        ".csv": "csv",
        ".xlsx": "excel",
        ".xls": "excel",
        ".json": "json",
        ".xml": "xml",
        ".txt": "text",
        ".md": "markdown"
    }
    
    class Config:
        env_file = ".env"

settings = Settings()