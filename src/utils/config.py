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

# src/utils/config.py
from pydantic import BaseModel, validator

class FinancialConfig(BaseModel):
    MIN_AGE: int = 18
    MAX_AGE: int = 100
    MIN_AMOUNT: float = 0
    MAX_AMOUNT: float = 1000000000
    DEFAULT_INFLATION_RATE: float = 3.0
    DEFAULT_RETURN_RATE: float = 7.0

    @validator('MIN_AGE')
    def validate_min_age(cls, v):
        if v < 0:
            raise ValueError("Minimum age cannot be negative")
        return v

    @validator('MAX_AGE')
    def validate_max_age(cls, v, values):
        if v <= values['MIN_AGE']:
            raise ValueError("Maximum age must be greater than minimum age")
        return v